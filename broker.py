from nmflows.peermatrix import PeeringMatrix, PeeringMatrixException
from nmflows.utils import MACDirectory, StatLogger
from nmflows.mq import RecvQueue
from nmflows.backend import RRDBackend
from config import CONFIG
from daemonize import Daemonize
import json
import jsonpickle
import threading
from datetime import datetime, timedelta
import time
import math


def handle_msg(ch, method, properties, body):
    try:
        with Lock:
            flow = jsonpickle.decode((json.loads(body)))
            Matrix.add_flow(flow)
    except PeeringMatrixException as e:
        Stats.increment_counter(e)
    except Exception as e:
        Stats.error(f"Unknown error while adding flow: {e}")


def consume_task():
    Queue.consume()


def flush_task():

    Stats.info("syncing to 5 minutes interval")
    delta = timedelta(minutes=5)
    now = datetime.now()
    next_date = datetime.min + math.ceil((now - datetime.min) / delta) * delta
    timesleep = (next_date.minute - now.minute - 1) * 60 + (60 - now.second)
    time.sleep(timesleep)

    while True:
        try:
            with Lock:
                Matrix.dump(CONFIG['bgp_matrix_dump'])
                Matrix.flush()
                Stats.log_counters()
                Stats.reset_counters()
        except Exception as e:
            Stats.error(f"Error while flushing matrix: {e}")
            continue
        finally:
            time.sleep(300)


def do_main():

    Stats.info("starting broker thread")
    t1 = threading.Thread(target=consume_task)
    t1.start()

    Stats.info("starting flushing thread")
    t2 = threading.Thread(target=flush_task)
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
