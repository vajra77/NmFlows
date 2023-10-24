

class UDPPacketHeader:

    def __init__(self, src_port, dst_port, p_len):
        self._source_port = src_port
        self._dest_port = dst_port
        self._payload_length = p_len

    @property
    def source_port(self):
        return self._source_port

    @property
    def dest_port(self):
        return self._dest_port

    @property
    def payload_length(self):
        return self._payload_length

    @classmethod
    def unpack(cls, data: bytes):
        src_port = int.from_bytes(data[0:2], 'big') & 0xffff
        dst_port = int.from_bytes(data[2:4], 'big') & 0xffff
        payload_length = int.from_bytes(data[4:6], 'big') & 0xffff
        return cls(src_port, dst_port, payload_length)

    def __repr__(self):
        return f"""
                                UDP Packet:
                                        Src Port: {self.source_port}
                                        Dst Port: {self.dest_port}
                                        Payload Len: {self.payload_length}
        """

