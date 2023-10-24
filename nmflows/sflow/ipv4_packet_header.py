import socket


class IPv4PacketHeader:

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
        ihl = int.from_bytes(data[0:1], 'big') & 0xf
        proto = int.from_bytes(data[9:10], 'big') & 0xffff
        src_addr = socket.inet_ntop(socket.AF_INET, data[12:16])
        dst_addr = socket.inet_ntop(socket.AF_INET, data[16:20])
        print(f"header is {ihl} long")
        return cls(src_addr, dst_addr, proto, 4 * ihl)

    def __repr__(self):
        return f"""
                                    Src Addr: {self.source_address}
                                    Dst Addr: {self.dest_address}
        """

