from nmflows.peermatrix import PeerMatrix
from nmflows.mq import RecvQueue
from nmflows.storage import StorableFlow
from config import CONFIG
import json
# import jsonpickle
import threading
import time


Matrix = PeerMatrix(CONFIG['ixf_url'])
Lock = threading.Lock()


def handle_msg(ch, method, properties, body):
    # flow = jsonpickle.decode(json.loads(body))
    flow = StorableFlow.from_pmacct_json(json.loads(body))
    with Lock:
        Matrix.add_flow(flow)


def consume_task():
    queue = RecvQueue(CONFIG['rabbitmq_host'],
                      CONFIG['rabbitmq_port'],
                      CONFIG['rabbitmq_queue'],
                      CONFIG['rabbitmq_user'],
                      CONFIG['rabbitmq_pass'],
                      handle_msg)
    queue.consume()


def dump_task():
    while True:
        time.sleep(5)
        with Lock:
            Matrix.dump(CONFIG['elastic_url'])


if __name__ == '__main__':
    try:
        t1 = threading.Thread(target=consume_task)
        t2 = threading.Thread(target=dump_task)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    except KeyboardInterrupt:
        exit()
