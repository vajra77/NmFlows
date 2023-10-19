

class SFlowSample:

    def __init__(self, sformat, length):
        self._format = sformat
        self._length = length

    @property
    def format(self):
        return self._format

    @property
    def length(self):
        return self._length
