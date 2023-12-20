from .sample import Sample


class FlowSample(Sample):

    def __init__(self, sformat, length):
        super().__init__(sformat, length)


    @classmethod
    def from_bytes(cls, sformat, length, data):
        pass

