from nmflows.sflow import SFlowDatagram
from nmflows.utils import PtrBuffer
from nmflows.storage import StorableFlow
from nmflows.mq import SendQueue
from config import CONFIG
from daemonize import Daemonize
import logging
import socketserver
import json
import jsonpickle
import sys


DEFAULT_BUFFER_SIZE = 4096  # 4k
DEBUG = False

def create_sflow_datagram(data: PtrBuffer):
    version = data.read_uint()
    if version != 5:
        raise Exception(f"sFlow version not supported: v{version}")
    return SFlowDatagram.unpack(version, data)


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
            for sample in datagram.samples:
                rate = sample.sampling_rate
                timestamp = sample.timestamp
                try:
                    for record in sample.records:
                        flow = StorableFlow.from_record(timestamp, rate, record)
                        queue.send(json.dumps(jsonpickle.encode(flow)))
                except AttributeError:
                    continue
        except EOFError:
            if DEBUG:
                print("[ERROR]: EOF while reading buffer", file=sys.stderr)
            return
        except Exception as e:
            if DEBUG:
                print(f"[ERROR]: {e}", file=sys.stderr)
            return

def do_main():
    server = socketserver.ThreadingUDPServer((CONFIG['sflow_listener_address'],
                                              CONFIG['sflow_listener_port']),
                                             ThisUDPRequestHandler)
    try:
        server.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        server.shutdown()
        server.server_close()
        exit()

if __name__ == "__main__":
    pid = "/tmp/nmflows-collector.pid"
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    fh = logging.FileHandler("/tmp/nmflows-collector.log", "w")
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    keep_fds = [fh.stream.fileno()]

    daemon = Daemonize(app="nmflows-collector", pid=pid, action=do_main, keep_fds=keep_fds)
    daemon.start()
