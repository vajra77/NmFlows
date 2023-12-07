import pika


class Queue:

    def __init__(self, host, port, name, credentials):
        self._host = host
        self._port = port
        self._name = name
        self._parameters = pika.ConnectionParameters(host=host, port=port,
                                                     virtual_host='/',
                                                     credentials=credentials,
                                                     heartbeat=600,
                                                     blocked_connection_timeout=300)

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def name(self):
        return self._name
