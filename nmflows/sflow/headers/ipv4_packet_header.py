import socket
import sys


class IPv4PacketHeader:

    def __init__(self, src_addr, dst_addr, proto, length, p_len):
        self._src_addr = src_addr
        self._dst_addr = dst_addr
        self._proto = proto
        self._length = length
        self._payload_length = p_len

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

    @property
    def payload_length(self):
        return self._payload_length

    @classmethod
    def unpack(cls, data: bytes):
        ihl = 4 * (int.from_bytes(data[0:1], byteorder=sys.byteorder, signed=False) & 0xf)
        proto = int.from_bytes(data[9:10], sys.byteorder, signed=False) & 0xff
        src_addr = socket.inet_ntop(socket.AF_INET, data[12:16])
        dst_addr = socket.inet_ntop(socket.AF_INET, data[16:20])
        t_length = int.from_bytes(data[2:4], byteorder=sys.byteorder, signed=False) & 0xffff
        return cls(src_addr, dst_addr, proto, ihl, t_length - ihl)

    def __repr__(self):
        return f"""
                                    Src Addr: {self.src_addr}
                                    Dst Addr: {self.dst_addr}
                                    Payload Len: {self.payload_length}
        """
