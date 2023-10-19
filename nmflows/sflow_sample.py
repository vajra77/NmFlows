from .flow_sample import FlowSample
import xdrlib


PROTO_ETHERNET = 1
PROTO_IPV4 = 11
PROTO_IPV6 = 12

FORMAT_FLOW_SAMPLE = (0, 1)
FORMAT_COUNTER_SAMPLE = (0, 2)
FORMAT_EXPANDED_FLOW_SAMPLE = (0, 3)

class SFlowSample:

    def __init__(self, s_format, length, data):
        self._format = s_format
        self._length = length
        self._data = data

    @property
    def format(self):
        return self._format

    @property
    def length(self):
        return self._length

    @property
    def data(self):
        return self._data

    @classmethod
    def unpack(cls, upx: xdrlib.Unpacker):
        f_bits = upx.unpack_uint()
        s_format = f_bits & 0b111111111111
        enterprise = (f_bits >> 12) & 0b11111111111111111111
        length = upx.unpack_uint()
        if (enterprise, s_format) == FORMAT_FLOW_SAMPLE:
            data = FlowSample.unpack(upx)
            return cls((enterprise, s_format), length, data)
        else:
            upx.unpack_fopaque(length)
            return None

    def __repr__(self):
        return f"""
                Class: {self.__class__.__name__}
                Format: {self.format}
                Length: {self.length} 
                Data: {self.data}       
        """
