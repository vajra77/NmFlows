from nmflows.parser import SFlowDatagram
from nmflows.utils import StatLogger, StorableFlow
from nmflows.mq import SendQueue
from config import CONFIG
from daemonize import Daemonize
import socketserver
import json
import jsonpickle
import threading
import time


DEFAULT_BUFFER_SIZE = 8192  # 8k


def do_stats():
    while True:
        time.sleep(300)
        Stats.log_counters()
        Stats.reset_counters()

class ThisUDPRequestHandler(socketserver.DatagramRequestHandler):

    def handle(self):
        data = self.socket.recv(DEFAULT_BUFFER_SIZE)
        queue = SendQueue(CONFIG['rabbitmq_host'],
                          CONFIG['rabbitmq_port'],
                          CONFIG['rabbitmq_queue'],
                          CONFIG['rabbitmq_user'],
                          CONFIG['rabbitmq_pass'])
        try:
            datagram = SFlowDatagram.from_bytes(data, Stats)
            Stats.increment_counter('processed_datagrams')
            for sample in datagram.samples:
                rate = sample.sampling_rate
                try:
                    for record in sample.records:
                        flow = StorableFlow.from_record(rate, record)
                        Stats.debug(flow)
                        Stats.increment_counter('processed_records')
                        queue.send(json.dumps(jsonpickle.encode(flow)))
                except AttributeError:
                    continue
        except Exception as e:
            Stats.debug(e)
            return


def do_main():

    server = socketserver.ThreadingUDPServer((CONFIG['sflow_listener_address'],
                                              CONFIG['sflow_listener_port']),
                                             ThisUDPRequestHandler)
    try:
        Stats.info("starting stats collector")
        st = threading.Thread(target=do_stats)
        st.start()
        Stats.info("starting UDP server")
        server.serve_forever()
        st.join()
    except Exception as e:
        Stats.error(f"received exception: {e}")
        server.shutdown()
        server.server_close()
        return


if __name__ == "__main__":

    Stats = StatLogger(CONFIG['collector_log'], CONFIG['debug'])
    daemon = Daemonize(app="nmflows-collector", pid=CONFIG['collector_pid'], action=do_main, keep_fds=Stats.keep_fds)
    daemon.start()
