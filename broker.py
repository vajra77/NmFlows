from nmflows.peermatrix import PeeringMatrix
from nmflows.mq import RecvQueue
from config import CONFIG
from daemonize import Daemonize
import logging
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
            Matrix.dump('/tmp/bgp-matrix.txt')
            Matrix.flush()


def do_main():
    t1 = threading.Thread(target=consume_task)
    t2 = threading.Thread(target=flush_task)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == "__main__":
    pid = "/tmp/nmflows-broker.pid"
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    fh = logging.FileHandler("/tmp/nmflows-broker.log", "w")
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    keep_fds = [fh.stream.fileno()]

    daemon = Daemonize(app="nmflows-broker", pid=pid, action=do_main, keep_fds=keep_fds)
    daemon.start()
