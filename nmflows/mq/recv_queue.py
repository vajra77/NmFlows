from .queue import Queue
import pika


class RecvQueue(Queue):

    def __init__(self, host, port, name, user, passw, callback):
        super().__init__(host, port, name)
        credentials = pika.PlainCredentials(user, passw)
        parameters = pika.ConnectionParameters(host, port, '/', credentials)
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()
        self._channel.basic_consume(queue=self._name,
                                    auto_ack=True,
                                    on_message_callback=callback)

    def consume(self):
        self._channel.start_consuming()