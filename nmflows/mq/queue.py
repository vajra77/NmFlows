

class Queue:

    def __init__(self, host, port, name):
        self._host = host
        self._port = port
        self._name = name

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def name(self):
        return self._name
