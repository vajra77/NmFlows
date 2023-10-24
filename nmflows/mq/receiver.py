import pika

class RecvQueue:

    def __init__(self, host, queue, user, passw, callback):
        self._host = host
        self._queue = queue
        credentials = pika.PlainCredentials(user, passw)
        parameters = pika.ConnectionParameters(host, 5672, '/', credentials)
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()
        self._channel.basic_consume(queue=self._queue,
                              auto_ack=True,
                              on_message_callback=callback)
