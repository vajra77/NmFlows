from .flow_sample import FlowSample
import xdrlib


FORMAT_FLOW_SAMPLE = 1
FORMAT_COUNTER_SAMPLE = 2
FORMAT_EXPANDED_FLOW_SAMPLE = 3


def create_sflow_sample(upx: xdrlib.Unpacker):
    sformat = upx.unpack_uint()
    length = upx.unpack_uint()
    if sformat == FORMAT_FLOW_SAMPLE:
        return FlowSample.unpack(sformat, length, upx)
    else:
        upx.unpack_fopaque(length)
        return None

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
