from nmflows.sflow import SFlowDatagram
from nmflows.utils import PtrBuffer, StatLogger
from nmflows.storage import StorableFlow
from nmflows.mq import SendQueue
from config import CONFIG
from daemonize import Daemonize
import socketserver
import json
import jsonpickle
import threading
from time import sleep

DEFAULT_BUFFER_SIZE = 8192  # 8k


def do_stats():
    while True:
        sleep(300)
        Stats.log_counters()
        Stats.reset_counters()

def create_sflow_datagram(data: PtrBuffer):
    version = data.read_uint()
    if version != 5:
        raise Exception(f"sFlow version not supported: v{version}")
    return SFlowDatagram.unpack(version, data, Stats)


class ThisUDPRequestHandler(socketserver.DatagramRequestHandler):

    def handle(self):
        data = self.socket.recv(DEFAULT_BUFFER_SIZE)
        queue = SendQueue(CONFIG['rabbitmq_host'],
                          CONFIG['rabbitmq_port'],
                          CONFIG['rabbitmq_queue'],
                          CONFIG['rabbitmq_user'],
                          CONFIG['rabbitmq_pass'])
        try:
            datagram = create_sflow_datagram(PtrBuffer(data, DEFAULT_BUFFER_SIZE))
            Stats.increment_counter('processed_datagrams')
            for sample in datagram.samples:
                rate = sample.sampling_rate
                timestamp = sample.timestamp
                try:
                    for record in sample.records:
                        flow = StorableFlow.from_record(timestamp, rate, record)
                        Stats.debug(f"received: {flow}")
                        queue.send(json.dumps(jsonpickle.encode(flow)))
                except AttributeError:
                    continue
        except EOFError:
            Stats.increment_counter('eof_errors')
            Stats.debug("EOF while reading buffer")
            return
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
