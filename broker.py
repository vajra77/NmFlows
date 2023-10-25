from nmflows.mq import RecvQueue
from nmflows.storage import StorableFlow
import json
import jsonpickle
import sys


def handle_msg(ch, method, properties, body):
    flow = jsonpickle.decode(json.loads(body))
    print(flow)



if __name__ == "__main__":
    HOST = sys.argv[1]
    USER = sys.argv[2]
    PASS = sys.argv[3]
    queue = RecvQueue(HOST, 'nmflows', USER, PASS, handle_msg)
