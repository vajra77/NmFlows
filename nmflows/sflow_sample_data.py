import xdrlib


class SFlowSampleData:

    def __init__(self):
        pass


    @classmethod
    def unpack(cls, length, upx: xdrlib.Unpacker):
        raise NotImplementedError
