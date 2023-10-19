from .flow_record import FlowRecord
from .ethernet_frame_header import EthernetFrameHeader
import xdrlib


PROTO_ETHERNET = 1
PROTO_IPV4 = 11
PROTO_IPV6 = 12


class RawPacketHeader(FlowRecord):

    def __init__(self, r_format, length, proto, content_length, stripped, header_length, header):
        super().__init__(r_format, length)
        self._proto = proto
        self._content_length = content_length
        self._stripped = stripped
        self._header_length = header_length
        self._header = header

    @property
    def proto(self):
        return self._proto

    @property
    def content_length(self):
        return self._content_length

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
    def unpack(cls, rformat, rlength, upx: xdrlib.Unpacker):
        proto = upx.unpack_uint()
        length = upx.unpack_uint()
        stripped = upx.unpack_uint()
        header_length = upx.unpack_uint()
        if proto == PROTO_ETHERNET:
            header = EthernetFrameHeader.unpack(upx, header_length)
            return cls(rformat, rlength, proto, length, stripped, header_length, header)
        else:
            upx.unpack_fopaque(header_length)
            return None

    def __repr__(self):
        return f"""
                                Class: {self.__class__.__name__}
                                Proto: {self.proto}
                                Length: {self.length}
                                Content Length: {self.content_length}
                                Stripped: {self.stripped}
                                Header Length: {self.header_length}
                                Header: {self.header}
        """