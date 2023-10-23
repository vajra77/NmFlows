from nmflows import SFlowDatagram, PtrBuffer
import socketserver
from pprint import pprint
import sys


DEFAULT_BUFFER_SIZE = 4096

def create_sflow_datagram(data: PtrBuffer):
    version = data.read_uint()
    if version != 5:
        raise Exception(f"sFlow version not supported: v{version}")
    return SFlowDatagram.unpack(version, data)

class ThisUDPRequestHandler(socketserver.DatagramRequestHandler):

    def handle(self):
        data = self.socket.recv(DEFAULT_BUFFER_SIZE)
        try:
            buffer = PtrBuffer(data, DEFAULT_BUFFER_SIZE)
            datagram = create_sflow_datagram(buffer)
            pprint(datagram)
        except EOFError:
            print("[ERROR]: EOF while reading buffer", file=sys.stderr)
        except Exception as e:
            print(f"[ERROR]: {e}", file=sys.stderr)


if __name__ == "__main__":
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    server = socketserver.ThreadingUDPServer((HOST, PORT), ThisUDPRequestHandler)

    try:
        server.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        server.shutdown()
        server.server_close()
        exit()
