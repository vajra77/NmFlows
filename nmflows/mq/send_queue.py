from .queue import Queue
import pika


class SendQueue(Queue):

    def __init__(self, host, port, name, user, passw):
        super().__init__(host, port, name)
        credentials = pika.PlainCredentials(user, passw)
        parameters = pika.ConnectionParameters(host=host, port=port,
                                               virtual_host='/',
                                               credentials=credentials,
                                               heartbeat=600,
                                               blocked_connection_timeout=300)
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()
        self._channel.queue_declare(name)

    def send(self, msg):
        self._channel.basic_publish(
            exchange='',
            routing_key=self._name,
            body=msg
        )

    def close(self):
        self._connection.close()

    def __del__(self):
        self.close()
