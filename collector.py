from nmflows.sflow import SFlowDatagram
from nmflows.utils import PtrBuffer
from nmflows.storage import StorableFlow
from nmflows.mq import SendQueue
from config import CONFIG
import traceback
import socketserver
import json
import jsonpickle
import sys


DEFAULT_BUFFER_SIZE = 4096  # 4k


def create_sflow_datagram(data: PtrBuffer):
    version = data.read_uint()
    if version != 5:
        raise Exception(f"sFlow version not supported: v{version}")
    return SFlowDatagram.unpack(version, data)


class ThisUDPRequestHandler(socketserver.DatagramRequestHandler):

    def handle(self):
        data = self.socket.recv(DEFAULT_BUFFER_SIZE)
        try:
            queue = SendQueue(CONFIG['rabbitmq_host'],
                              CONFIG['rabbitmq_port'],
                              CONFIG['rabbitmq_queue'],
                              CONFIG['rabbitmq_user'],
                              CONFIG['rabbitmq_pass'])
            datagram = create_sflow_datagram(PtrBuffer(data, DEFAULT_BUFFER_SIZE))
            for sample in datagram.samples:
                rate = sample.sampling_rate
                timestamp = sample.timestamp
                try:
                    for record in sample.records:
                        flow = StorableFlow.from_record(timestamp, rate, record)
                        # queue.send(flow.to_pmacct_json())
                        queue.send(json.dumps(jsonpickle.encode(flow)))
                except AttributeError:
                    continue
        except EOFError:
            print("[ERROR]: EOF while reading buffer", file=sys.stderr)
        except Exception as e:
            print(f"[ERROR]: {e}", file=sys.stderr)
            traceback.print_exc()


if __name__ == "__main__":
    server = socketserver.ThreadingUDPServer((CONFIG['sflow_listener_address'],
                                              CONFIG['sflow_listener_port']),
                                             ThisUDPRequestHandler)
    try:
        server.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        server.shutdown()
        server.server_close()
        exit()
