from nmflows.mq import RecvQueue
from config import CONFIG
import json
import jsonpickle
import sys


def handle_msg(ch, method, properties, body):
    flow = jsonpickle.decode(json.loads(body))
    print(flow)


def main():
    queue = RecvQueue(CONFIG['rabbitmq_host'],
                      CONFIG['rabbitmq_port'],
                      CONFIG['rabbitmq_queue'],
                      CONFIG['rabbitmq_user'],
                      CONFIG['rabbitmq_pass'],
                      handle_msg)
    queue.consume()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            exit()
