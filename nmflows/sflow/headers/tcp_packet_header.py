import sys


class TCPPacketHeader:

    def __init__(self, src_port, dst_port):
        self._src_port = src_port
        self._dst_port = dst_port

    @property
    def src_port(self):
        return self._src_port

    @property
    def dst_port(self):
        return self._dst_port

    @classmethod
    def unpack(cls, data: bytes):
        src_port = int.from_bytes(data[0:2], byteorder='big', signed=False) & 0xffff
        dst_port = int.from_bytes(data[2:4], byteorder='big', signed=False) & 0xffff
        return cls(src_port, dst_port)

    def __repr__(self):
        return f"""
                                    TCP Packet:
                                        Src Port: {self.src_port}
                                        Dst Port: {self.dst_port}
        """

