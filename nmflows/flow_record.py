from .ethernet_frame_data import EthernetFrameData
from .raw_frame_header import RawFrameHeader
import xdrlib

FORMAT_RAW_HEADER = 1
FORMAT_ETHERNET_DATA = 2
FORMAT_IPV4_DATA = 3
FORMAT_IPV6_DATA = 4


class FlowRecord:

    def __init__(self, r_format, length, data):
        self._format = r_format
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
        rformat = upx.unpack_uint()
        length = upx.unpack_uint()
        if rformat == FORMAT_ETHERNET_DATA:
            assert length == 16, "EthernetFrameData has wrong length"
            data = EthernetFrameData.unpack(upx)
            return cls((enterprise, s_format), length, data)
        elif rformat == FORMAT_RAW_HEADER:
            data = RawFrameHeader.unpack(upx)
            if data is not None:
                return cls(rformat, length, data)
        else:
            upx.unpack_fopaque(length)
            return None

    def __repr__(self):
        return f"""
                        Format: {self.format}
                        Length: {self.length}
                        Data: {self.data}
        """
