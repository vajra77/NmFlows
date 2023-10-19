import socketserver, threading, time
from pprint import pprint
from nmflows import SFlowDatagram
import xdrlib


def create_sflow_datagram(upx: xdrlib.Unpacker):
    version = upx.unpack_uint()
    if version != 5:
        raise Exception(f"sFlow version not supported: v{version}")
    return SFlowDatagram.unpack(version, upx)


class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        # socket = self.request[1]
        # current_thread = threading.current_thread()
        try:
            unpacker = xdrlib.Unpacker(data)
            datagram = create_sflow_datagram(unpacker)
        except Exception as e:
            print(f"[ERROR]: {e}")
        else:
            pprint(datagram)


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 5510

    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True

    try:
        server_thread.start()
        print("Server started at {} port {}".format(HOST, PORT))
        while True: time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        server.shutdown()
        server.server_close()
        exit()