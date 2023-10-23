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
    def unpack(cls, data: bytes):
        h1 = data[0:4]
        h2 = data[4:8]
        h3 = data[8:12]
        src_addr = socket.inet_ntop(socket.AF_INET, data[12:16])
        dst_addr = socket.inet_ntop(socket.AF_INET, data[16:20])
        options = data[20:24]
        return cls(src_addr, dst_addr, 24)

    def __repr__(self):
        return f"""
                                    Src Addr: {self.source_address}
                                    Dst Addr: {self.dest_address}
        """

