

class FlowRecord:

    def __init__(self, r_format, length):
        self._format = r_format
        self._length = length

    @property
    def format(self):
        return self._format

    @property
    def length(self):
        return self._length
