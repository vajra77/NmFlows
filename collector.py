from nmflows.sflow import SFlowDatagram, SFlowStats
from nmflows.utils import PtrBuffer
from nmflows.storage import StorableFlow
from nmflows.mq import SendQueue
from config import CONFIG
from daemonize import Daemonize
import logging
import socketserver
import json
import jsonpickle
import threading
from time import sleep
from datetime import datetime

DEFAULT_BUFFER_SIZE = 8192  # 8k


def do_stats():
    while True:
        sleep(300)
        now = datetime.now()
        logger.info(f"STATS[{now}]: {stats}")


def create_sflow_datagram(data: PtrBuffer):
    version = data.read_uint()
    if version != 5:
        stats.unsupported_version += 1
        raise Exception(f"sFlow version not supported: v{version}")
    return SFlowDatagram.unpack(version, data, stats)


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
            stats.processed_datagrams += 1
            for sample in datagram.samples:
                rate = sample.sampling_rate
                timestamp = sample.timestamp
                try:
                    for record in sample.records:
                        flow = StorableFlow.from_record(timestamp, rate, record)
                        logger.debug(f"[RCVD]: {flow}")
                        queue.send(json.dumps(jsonpickle.encode(flow)))
                except AttributeError:
                    continue
        except EOFError:
            stats.eof_errors += 1
            logger.debug("[EXC] EOF while reading buffer")
            return
        except Exception as e:
            logger.debug(f"[EXC]: {e}")
            return


def do_main():
    server = socketserver.ThreadingUDPServer((CONFIG['sflow_listener_address'],
                                              CONFIG['sflow_listener_port']),
                                             ThisUDPRequestHandler)
    try:
        st = threading.Thread(target=do_stats)
        st.start()
        server.serve_forever()
        st.join()
    except Exception as e:
        logger.error(f"Received exception: {e}")
        server.shutdown()
        server.server_close()
        return


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    if CONFIG['debug']:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    logger.propagate = False
    fh = logging.FileHandler(CONFIG['collector_log'], "w")

    if CONFIG['debug']:
        fh.setLevel(logging.DEBUG)
    else:
        fh.setLevel(logging.INFO)

    logger.addHandler(fh)
    keep_fds = [fh.stream.fileno()]

    stats = SFlowStats()

    logger.info("starting collector")
    daemon = Daemonize(app="nmflows-collector", pid=CONFIG['collector_pid'], action=do_main, keep_fds=keep_fds)
    daemon.start()
