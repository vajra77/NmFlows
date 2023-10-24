import pika


class SendQueue:

    def __init__(self, host, queue):
        self._host = host
        self._queue = queue
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue)

    def send(self, msg):
        self._channel.basic_publish(
            exchange='',
            routing_key=self._queue,
            body=msg
        )
