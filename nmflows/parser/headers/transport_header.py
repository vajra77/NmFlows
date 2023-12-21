from nmflows.utils.buffer import Buffer
from .network_header import NetworkHeader


class TransportHeader:

    def __init__(self, proto, length, tot_len, src_port, dst_port):
        self._proto = proto
        self._length = length
        if tot_len == 0:
            self._payload_length = 0
        else:
            self._payload_length = tot_len - length
        self._source_port = src_port
        self._destination_port = dst_port

    @property
    def proto(self):
        return self._proto

    @property
    def length(self):
        return self._length

    @property
    def payload_length(self):
        return self._payload_length

    @property
    def source_port(self):
        return self._source_port

    @property
    def destination_port(self):
        return self._destination_port

    @property
    def is_unknown(self):
        return (self._length == 0
                and self._payload_length == 0
                and self._source_port == 0
                and self._destination_port == 0)

    @classmethod
    def from_bytes(cls, data, proto):
        buffer = Buffer.from_bytes(data)
        if proto == NetworkHeader.UPPER_PROTO_TCP:
            # TCP Packet Header
            src_port = buffer.read_short(0)
            dst_port = buffer.read_short(2)
            return cls(proto, 20, 0, src_port, dst_port)
        elif proto == NetworkHeader.UPPER_PROTO_UDP:
            # UDP Packet Header
            src_port = buffer.read_short(0)
            dst_port = buffer.read_short(2)
            tot_len = buffer.read_short(4)
            return cls(proto, 8, tot_len, src_port, dst_port)
        else:
            return cls.unknown(proto)

    @classmethod
    def unknown(cls, proto):
        return cls(proto, 0, 0, 0, 0)
