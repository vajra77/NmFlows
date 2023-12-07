from .queue import Queue
import pika


class SendQueue(Queue):

    def __init__(self, host, port, name, user, passw):
        super().__init__(host, port, name, pika.PlainCredentials(user, passw))
        self._connection = pika.BlockingConnection(self._parameters)
        self._channel = self._connection.channel()
        self._channel.queue_declare(self._name)

    def send(self, msg):
        # connection = pika.BlockingConnection(self._parameters)
        # channel = connection.channel()
        # channel.queue_declare(self._name)
        self._channel.basic_publish(
            exchange='',
            routing_key=self._name,
            body=msg
        )

    def close(self):
        self._connection.close()

    def __del__(self):
        self.close()
