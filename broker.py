from nmflows.mq import RecvQueue
# from nmflows.storage import StorableFlow
import json
import jsonpickle
import os
import sys


def handle_msg(ch, method, properties, body):
    flow = jsonpickle.decode(json.loads(body))
    print(flow)

def main(host, user, passw):
    queue = RecvQueue(HOST, 'nmflows', USER, PASS, handle_msg)
    queue.consume()


if __name__ == '__main__':
    HOST = sys.argv[1]
    USER = sys.argv[2]
    PASS = sys.argv[3]

    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
