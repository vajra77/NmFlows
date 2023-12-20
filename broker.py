from nmflows.peermatrix import PeeringMatrix, PeeringMatrixException
from nmflows.utils import MACDirectory, StatLogger
from nmflows.mq import RecvQueue
from nmflows.backend import RRDBackend
from config import CONFIG
from daemonize import Daemonize
import json
import jsonpickle
import threading
import datetime
import time


def handle_msg(ch, method, properties, body):
    try:
        with Lock:
            flow = jsonpickle.decode((json.loads(body)))
            Matrix.add_flow(flow)
    except PeeringMatrixException as e:
        Stats.debug(f"[ERROR]: {e}")
    except Exception as e:
        Stats.error(f"Unknown error while adding flow: {e}")


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
            Stats.error(f"Error while flushing matrix: {e}")
            continue


def do_main():
    sleeptime = 300 - datetime.datetime.utcnow().second
    time.sleep(sleeptime)

    t1 = threading.Thread(target=consume_task)
    t2 = threading.Thread(target=flush_task)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == "__main__":

    Stats = StatLogger(CONFIG['broker_log'], CONFIG['debug'])

    Matrix = PeeringMatrix(MACDirectory(CONFIG['ixf_url']),
                           RRDBackend(CONFIG['rrd_base_path'], CONFIG['rrd_graph_gamma']))
    Lock = threading.Lock()
    Queue = RecvQueue(CONFIG['rabbitmq_host'],
                      CONFIG['rabbitmq_port'],
                      CONFIG['rabbitmq_queue'],
                      CONFIG['rabbitmq_user'],
                      CONFIG['rabbitmq_pass'],
                      handle_msg)

    daemon = Daemonize(app="nmflows-broker", pid=CONFIG['broker_pid'], action=do_main, keep_fds=Stats.keep_fds)
    daemon.start()
