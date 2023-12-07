from .queue import Queue
import pika


class RecvQueue(Queue):

    def __init__(self, host, port, name, user, passw, callback):
        super().__init__(host, port, name, pika.PlainCredentials(user, passw))
        self._callback = callback

    def consume(self):
        connection = pika.BlockingConnection(self._parameters)
        channel = connection.channel()
        channel.basic_consume(queue=self.name,
                              auto_ack=True,
                              on_message_callback=self._callback)
        channel.start_consuming()
