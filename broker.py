from nmflows.peermatrix import PeeringMatrix
from nmflows.mq import RecvQueue
from config import CONFIG
import json
import jsonpickle
import threading
import time


def handle_msg(ch, method, properties, body):
    with Lock:
        Matrix.add_flow(jsonpickle.decode(json.loads(body)))

def consume_task():
    Queue.consume()

Matrix = PeeringMatrix(CONFIG['ixf_url'], CONFIG['elastic_url'])
Lock = threading.Lock()
Queue = RecvQueue(CONFIG['rabbitmq_host'],
                      CONFIG['rabbitmq_port'],
                      CONFIG['rabbitmq_queue'],
                      CONFIG['rabbitmq_user'],
                      CONFIG['rabbitmq_pass'],
                      handle_msg)

def flush_task():
    while True:
        time.sleep(300)
        with Lock:
            Matrix.flush()


if __name__ == '__main__':
    try:
        t1 = threading.Thread(target=consume_task)
        t2 = threading.Thread(target=flush_task)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    except KeyboardInterrupt:
        exit()
