from .queue import Queue
import pika


class SendQueue(Queue):

    def __init__(self, host, port, name, user, passw):
        super().__init__(host, port, name)
        credentials = pika.PlainCredentials(user, passw)
        parameters = pika.ConnectionParameters(host, port, '/', credentials)
        print(f"connecting to {host}:{port} with user {user} and pass {passw}")
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()
        self._channel.queue_declare(name)

    def send(self, msg):
        self._channel.basic_publish(
            exchange='',
            routing_key=self._name,
            body=msg
        )
