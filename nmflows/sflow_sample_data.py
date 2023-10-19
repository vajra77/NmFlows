from .flow_sample import FlowSample
import xdrlib


PROTO_ETHERNET = 1
PROTO_IPV4 = 11
PROTO_IPV6 = 12

FORMAT_FLOW_SAMPLE = 1
FORMAT_COUNTER_SAMPLE = 2
FORMAT_EXPANDED_FLOW_SAMPLE = 3

class SFlowSampleData:

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
        s_format = upx.unpack_uint()
        length = upx.unpack_uint()
        if s_format == FORMAT_FLOW_SAMPLE:
            data = FlowSample.unpack(upx)
            return cls(s_format, length, data)
        else:
            print(f"Format (sample): {s_format}")
            upx.unpack_fopaque(length)
            return None

    def __repr__(self):
        return f"""
                Class: {self.__class__.__name__}
                Format: {self.format}
                Length: {self.length} 
                Data: {self.data}       
        """
