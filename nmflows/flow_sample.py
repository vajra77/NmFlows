import xdrlib
from .sflow_sample_data import SFlowSampleData


class FlowSample(SFlowSampleData):

    def __init__(self):
        super().__init__()

    @classmethod
    def unpack(cls, length, upx: xdrlib.Unpacker):
        pass