from .ethernet_frame_data import EthernetFrameData
import xdrlib


PROTO_ETHERNET = 1
PROTO_IPV4 = 11
PROTO_IPV6 = 12

class RawFrameHeader:

    def __init__(self, proto, length, stripped, header_length, header):
        self._proto = proto
        self._length = length
        self._stripped = stripped
        self._header_length = header_length
        self._header = header

    @property
    def proto(self):
        return self._proto

    @property
    def length(self):
        return self._length

    @property
    def stripped(self):
        return self._stripped

    @property
    def header_length(self):
        return self._header_length

    @property
    def header(self):
        return self._header

    @classmethod
    def unpack(cls, upx: xdrlib.Unpacker):
        proto = upx.unpack_uint()
        length = upx.unpack_uint()
        stripped = upx.unpack_uint()
        header_length = upx.unpack_uint()
        if proto == PROTO_ETHERNET:
            assert header_length == 16, "Ethernet Header has wrong length"
            header = EthernetFrameData.unpack(upx)
            return cls(proto, length, stripped, header_length, header)
        else:
            upx.unpack_fopaque(length)
            return None

    def __repr__(self):
        return f"""
                                Class: {self.__class__.__name__}
                                Proto: {self.proto}
                                Length: {self.length}
                                Stripped: {self.stripped}
                                Header Length: {self.header_length}
        """