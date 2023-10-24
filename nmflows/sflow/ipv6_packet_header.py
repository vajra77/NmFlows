import socket


class IPv6PacketHeader:

    def __init__(self, src_addr, dst_addr, proto, length):
        self._source_address = src_addr
        self._dest_address = dst_addr
        self._proto = proto
        self._length = length

    @property
    def source_address(self):
        return self._source_address

    @property
    def dest_address(self):
        return self._dest_address

    @property
    def proto(self):
        return self._proto

    @property
    def length(self):
        return self._length

    @classmethod
    def unpack(cls, data: bytes):
        proto = int.from_bytes(data[6:7], 'big')
        src_addr = socket.inet_ntop(socket.AF_INET6, data[8:24])
        dst_addr = socket.inet_ntop(socket.AF_INET6, data[24:40])
        return cls(src_addr, dst_addr, proto, 40)

    def __repr__(self):
        return f"""
                                    Src Addr: {self.source_address}
                                    Dst Addr: {self.dest_address}
        """

