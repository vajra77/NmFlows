import socket


class IPv6PacketHeader:

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
        src_addr = socket.inet_ntop(socket.AF_INET6, data[8:24])
        dst_addr = socket.inet_ntop(socket.AF_INET, data[24:30])
        return cls(src_addr, dst_addr, 30)

    def __repr__(self):
        return f"""
                                    Src Addr: {self.source_address}
                                    Dst Addr: {self.dest_address}
        """

