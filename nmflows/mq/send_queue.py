from .queue import Queue
import pika


class SendQueue(Queue):

    def __init__(self, host, port, name, user, passw):
        super().__init__(host, port, name)
        print("QUI 1")
        credentials = pika.PlainCredentials(user, passw)
        print("QUI 2")
        parameters = pika.ConnectionParameters(host, port, '/', credentials)
        print("QUI 3")
        self._connection = pika.BlockingConnection(parameters)
        print("QUI 4")
        self._channel = self._connection.channel()
        print("QUI 5")
        self._channel.queue_declare(name)

    def send(self, msg):
        self._channel.basic_publish(
            exchange='',
            routing_key=self._name,
            body=msg
        )
