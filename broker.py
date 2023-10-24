from nmflows.mq import RecvQueue
import sys


def handle_msg():
    pass

if __name__ == "__main__":
    HOST = sys.argv[1]
    USER = sys.argv[2]
    PASS = sys.argv[3]
    queue = RecvQueue(HOST, 'nmflows', USER, PASS, handle_msg)
