import socketserver, threading, time, sflow, binascii
from pprint import pprint
from nmflows import SFlowRawPacket



class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        # socket = self.request[1]
        # current_thread = threading.current_thread()
        try:
            dgram = SFlowRawPacket.unpack(data)
        except Exception as e:
            print(f"Caught exception: {e}")
        else:
            pprint(dgram)


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