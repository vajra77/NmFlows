import pika


class SendQueue:

    def __init__(self, host, queue, user, passw):
        self._host = host
        self._queue = queue
        credentials = pika.PlainCredentials(user, passw)
        parameters = pika.ConnectionParameters(host, 5672, '/', credentials)
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue)

    def send(self, msg):
        self._channel.basic_publish(
            exchange='',
            routing_key=self._queue,
            body=msg
        )
