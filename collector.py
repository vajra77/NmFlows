from nmflows import SFlowDatagram
import socketserver
from pprint import pprint
import xdrlib
import sys


def create_sflow_datagram(upx: xdrlib.Unpacker):
    version = upx.unpack_uint()
    if version != 5:
        raise Exception(f"sFlow version not supported: v{version}")
    return SFlowDatagram.unpack(version, upx)


class ThisUDPRequestHandler(socketserver.DatagramRequestHandler):

    def handle(self):
        data = self.socket.recv(1024)
        try:
            unpacker = xdrlib.Unpacker(data)
            datagram = create_sflow_datagram(unpacker)
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
