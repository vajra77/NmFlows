from nmflows.peermatrix import PeerMatrix
from nmflows.mq import RecvQueue
from config import CONFIG
import json
import jsonpickle
import threading
import time


matrix = PeerMatrix()
lock = threading.Lock()


def handle_msg(ch, method, properties, body):
    flow = jsonpickle.decode(json.loads(body))
    with lock:
        matrix.add_flow(flow)

def consume_task():
    queue = RecvQueue(CONFIG['rabbitmq_host'],
                      CONFIG['rabbitmq_port'],
                      CONFIG['rabbitmq_queue'],
                      CONFIG['rabbitmq_user'],
                      CONFIG['rabbitmq_pass'],
                      handle_msg)
    queue.consume()

def dump_task():
    time.sleep(5)
    with lock:
        matrix.dump(CONFIG['elastic_url'])

if __name__ == '__main__':
    try:
        t1 = threading.Thread(target=consume_task)
        t2 = threading.Thread(target=dump_task)
        t1.join()
        t2.join()
    except KeyboardInterrupt:
        exit()
