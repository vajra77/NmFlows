import socket


class IPv6PacketHeader:

    def __init__(self, src_addr, dst_addr, proto, length):
        self._src_addr = src_addr
        self._dst_addr = dst_addr
        self._proto = proto
        self._length = length

    @property
    def src_addr(self):
        return self._src_addr

    @property
    def dst_addr(self):
        return self._dst_addr

    @property
    def proto(self):
        return self._proto

    @property
    def length(self):
        return self._length

    @classmethod
    def unpack(cls, data: bytes):
        proto = int.from_bytes(data[6:7], 'big') & 0xff
        src_addr = socket.inet_ntop(socket.AF_INET6, data[8:24])
        dst_addr = socket.inet_ntop(socket.AF_INET6, data[24:40])
        return cls(src_addr, dst_addr, proto, 40)

    def __repr__(self):
        return f"""
                                    Src Addr: {self.src_addr}
                                    Dst Addr: {self.dst_addr}
        """

