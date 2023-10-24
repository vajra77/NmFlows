import socket


class TCPPacketHeader:

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
        src_port = socket.inet_ntop(socket.AF_INET, data[0:2])
        dst_port = socket.inet_ntop(socket.AF_INET, data[2:4])
        return cls(src_port, dst_port)

    def __repr__(self):
        return f"""
                                    TCP Packet:
                                        Src Port: {self.source_port}
                                        Dst Port: {self.dest_port}
        """

