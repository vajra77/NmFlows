

FORMAT_FLOW_SAMPLE = 1
FORMAT_COUNTER_SAMPLE = 2
FORMAT_EXPANDED_FLOW_SAMPLE = 3


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

    def is_flow_sample(self):
        return self._format == FORMAT_FLOW_SAMPLE

    def is_counter_sample(self):
        return self._format == FORMAT_COUNTER_SAMPLE

    def is_expanded_flow_sample(self):
        return self._format == FORMAT_EXPANDED_FLOW_SAMPLE
