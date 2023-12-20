import sys


class UDPPacketHeader:

    def __init__(self, src_port, dst_port, p_len):
        self._src_port = src_port
        self._dst_port = dst_port
        self._payload_length = p_len

    @property
    def src_port(self):
        return self._src_port

    @property
    def dst_port(self):
        return self._dst_port

    @property
    def payload_length(self):
        return self._payload_length

    @classmethod
    def unpack(cls, data: bytes):
        src_port = int.from_bytes(data[0:2], byteorder=sys.byteorder, signed=False) & 0xffff
        dst_port = int.from_bytes(data[2:4], byteorder=sys.byteorder, signed=False) & 0xffff
        payload_length = int.from_bytes(data[4:6], byteorder=sys.byteorder, signed=False) & 0xffff
        return cls(src_port, dst_port, payload_length)

    def __repr__(self):
        return f"""
                                    UDP Packet:
                                        Src Port: {self.src_port}
                                        Dst Port: {self.dst_port}
                                        Payload Len: {self.payload_length}
        """

