from nmflows.peermatrix import PeeringMatrix
from nmflows.utils import MACDirectory
from nmflows.mq import RecvQueue
from nmflows.backend import RRDBackend
from config import CONFIG
from daemonize import Daemonize
import logging
import json
import jsonpickle
import threading
import time


def handle_msg(ch, method, properties, body):
    try:
        with Lock:
            flow = jsonpickle.decode((json.loads(body)))
            Matrix.add_flow(flow)
    except Exception as e:
        logger.error(f"Error while adding flow: {flow}")


def consume_task():
    Queue.consume()


def flush_task():
    while True:
        time.sleep(300)
        try:
            with Lock:
                Matrix.dump(CONFIG['bgp_matrix_dump'])
                Matrix.flush()
        except Exception as e:
            logger.error(f"Error while flushing matrix: {e}")
            continue


def do_main():
    t1 = threading.Thread(target=consume_task)
    t2 = threading.Thread(target=flush_task)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    fh = logging.FileHandler(CONFIG['broker_log'], "w")
    if CONFIG['debug']:
        fh.setLevel(logging.DEBUG)
    else:
        fh.setLevel(logging.INFO)
    logger.addHandler(fh)
    keep_fds = [fh.stream.fileno()]

    Matrix = PeeringMatrix(MACDirectory(CONFIG['ixf_url']),
                           RRDBackend(CONFIG['rrd_base_path'], CONFIG['rrd_graph_gamma']))
    Lock = threading.Lock()
    Queue = RecvQueue(CONFIG['rabbitmq_host'],
                      CONFIG['rabbitmq_port'],
                      CONFIG['rabbitmq_queue'],
                      CONFIG['rabbitmq_user'],
                      CONFIG['rabbitmq_pass'],
                      handle_msg)

    daemon = Daemonize(app="nmflows-broker", pid=CONFIG['broker_pid'], action=do_main, keep_fds=keep_fds)
    daemon.start()
