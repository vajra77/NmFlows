

class UDPPacketHeader:

    def __init__(self, src_port, dst_port):
        self._source_port = src_port
        self._dest_port = dst_port

    @property
    def source_port(self):
        return self._source_port

    @property
    def dest_port(self):
        return self._dest_port

    @classmethod
    def unpack(cls, data: bytes):
        src_port = int.from_bytes(data[0:2], 'big') & 0xffff
        dst_port = int.from_bytes(data[2:4], 'big') & 0xffff
        return cls(src_port, dst_port)

    def __repr__(self):
        return f"""
                                        UDP Packet:
                                            Src Port: {self.source_port}
                                            Dst Port: {self.dest_port}
        """

