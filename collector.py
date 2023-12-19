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
import signal


DEFAULT_BUFFER_SIZE = 8192  # 8k


def do_stats(sig_value, _):
    logger.info(f"STATS: {stats}")


def create_sflow_datagram(data: PtrBuffer):
    version = data.read_uint()
    if version != 5:
        stats.inc_unsupported_version()
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
            stats.inc_processed_datagrams()
            for sample in datagram.samples:
                rate = sample.sampling_rate
                timestamp = sample.timestamp
                try:
                    for record in sample.records:
                        flow = StorableFlow.from_record(timestamp, rate, record)
                        if CONFIG['debug']:
                            logger.debug(f"[RCVD]: {flow}")
                        queue.send(json.dumps(jsonpickle.encode(flow)))
                except AttributeError:
                    continue
        except EOFError:
            stats.inc_eof_errors()
            if CONFIG['debug']:
                logger.error("[ERROR]: EOF while reading buffer")
            return
        except Exception as e:
            if CONFIG['debug']:
                logger.error(f"[ERROR]: {e}")
            return


def do_main():
    server = socketserver.ThreadingUDPServer((CONFIG['sflow_listener_address'],
                                              CONFIG['sflow_listener_port']),
                                             ThisUDPRequestHandler)
    try:
        signal.signal(signal.SIGUSR1, do_stats)
        server.serve_forever()
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
