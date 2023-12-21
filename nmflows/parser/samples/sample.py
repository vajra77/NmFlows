

class Sample:

    FORMAT_FLOW_SAMPLE = 1
    FORMAT_COUNTER_SAMPLE = 2
    FORMAT_EXT_FLOW_SAMPLE = 3
    FORMAT_EXT_COUNTER_SAMPLE = 4

    def __init__(self, sformat, length):
        self._format = sformat
        self._length = length

    @property
    def format(self):
        return self._format

    def length(self):
        return self._length
