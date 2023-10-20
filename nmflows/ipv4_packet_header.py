import socket
import xdrlib


class IPv4PacketHeader:

    def __init__(self, src_addr, dst_addr, length):
        self._source_address = src_addr
        self._dest_address = dst_addr
        self._length = length

    @property
    def source_address(self):
        return self._source_address

    @property
    def dest_address(self):
        return self._dest_address

    @property
    def length(self):
        return self._length

    @classmethod
    def unpack(cls, upx: xdrlib.Unpacker):
        h1 = upx.unpack_uint()
        h2 = upx.unpack_uint()
        h3 = upx.unpack_uint()
        src_addr = socket.inet_ntoa(upx.unpack_uint())
        dst_addr = socket.inet_ntoa(upx.unpack_uint())
        options = upx.unpack_uint()
        return cls(src_addr, dst_addr, 48)

