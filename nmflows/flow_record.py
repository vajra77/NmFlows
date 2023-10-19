from .ethernet_frame_data import EthernetFrameData
import xdrlib

FORMAT_RAW_HEADER = (0, 1)
FORMAT_ETHERNET_DATA = (0, 2)
FORMAT_IPV4_DATA = (0, 3)
FORMAT_IPV6_DATA = (0, 4)


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
        f_bits = upx.unpack_uint()
        s_format = f_bits & 0b111111111111
        enterprise = (f_bits >> 12) & 0b11111111111111111111
        length = upx.unpack_uint()
        if (enterprise, s_format) == FORMAT_ETHERNET_DATA:
            assert length == 16, "EthernetFrameData has wrong length"
            data = EthernetFrameData.unpack(upx)
            return cls((enterprise, s_format), length, data)
        elif (enterprise, s_format) == FORMAT_RAW_HEADER:
            print(f"Record is RAW")
            upx.unpack_fopaque(length)
        else:
            upx.unpack_fopaque(length)
            return None

    def __repr__(self):
        return f"""
                        Format: {self.format}
                        Length: {self.length}
                        Data: {self.data}
        """
