import pika

class RecvQueue:

    def __init__(self, host, queue, callback):
        self._host = host
        self._queue = queue
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self._channel = self._connection.channel()
        self._channel.basic_consume(queue=self._queue,
                              auto_ack=True,
                              on_message_callback=callback)
