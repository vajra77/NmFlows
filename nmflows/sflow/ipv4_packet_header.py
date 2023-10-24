import socket


class IPv4PacketHeader:

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
        ihl = int.from_bytes(data[0:1], 'big') & 0xf
        proto = int.from_bytes(data[9:10], 'big') & 0xffff
        src_addr = socket.inet_ntop(socket.AF_INET, data[12:16])
        dst_addr = socket.inet_ntop(socket.AF_INET, data[16:20])
        return cls(src_addr, dst_addr, proto, 4 * ihl)

    def __repr__(self):
        return f"""
                                    Src Addr: {self.src_addr}
                                    Dst Addr: {self.dst_addr}
        """

