from nmflows.sflow.raw_packet_header import RawPacketHeader

KNOWN_IP_PROTO = {
    2048: 'ipv4',
    34525: 'ipv6'
}

KNOWN_PORTS = {
    80: 'http',
    443: 'https',
    179: 'bgp',
    25: 'smtp',
    465: 'smtps',
    993: 'imap',
    22: 'ssh',
    53: 'dns'
}


def _ip(n: int):
    if n in KNOWN_IP_PROTO.keys():
        return KNOWN_IP_PROTO[n]
    else:
        return str(n)


def _pp(n: int):
    if n in KNOWN_PORTS.keys():
        return KNOWN_PORTS[n]
    else:
        return str(n)


class StorableFlow:

    def __init__(self, ts, rate, vlan, proto, src_mac, dst_mac, src_ip, dst_ip, src_port, dst_port, size):
        self._timestamp = ts
        self._sampling_rate = rate
        self._vlan = vlan
        self._proto = proto
        self._src_mac = src_mac
        self._dst_mac = dst_mac
        self._src_addr = src_ip
        self._dst_addr = dst_ip
        self._src_port = src_port
        self._dst_port = dst_port
        self._size = size

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def vlan(self):
        return self._vlan

    @property
    def proto(self):
        return self._proto

    @property
    def src_mac(self):
        return self._src_mac

    @property
    def dst_mac(self):
        return self._dst_mac

    @property
    def src_addr(self):
        return self._src_addr

    @property
    def dst_addr(self):
        return self._dst_addr

    @property
    def src_port(self):
        return self._src_port

    @property
    def dst_port(self):
        return self._dst_port

    @property
    def size(self):
        return self._size

    @property
    def sampling_rate(self):
        return self._sampling_rate

    @property
    def computed_size(self):
        return self._size * self._sampling_rate

    @classmethod
    def from_record(cls, timestamp, rate, record: RawPacketHeader):
        return cls(
            timestamp, rate,
            record.datalink_header.vlan,
            record.datalink_header.type,
            record.datalink_header.src_mac,
            record.datalink_header.dst_mac,
            record.network_header.src_addr,
            record.network_header.dst_addr,
            record.transport_header.src_port,
            record.transport_header.dst_port,
            record.payload_length
        )

    def to_json(self):
        return {
            'timestamp': self._timestamp,
            'sampling_rate': self._sampling_rate,
            'vlan': self._vlan,
            'proto': self._proto,
            'src_mac': self._src_mac,
            'dst_mac': self._dst_mac,
            'src_addr': self._src_addr,
            'dst_addr': self._dst_addr,
            'src_port': self._src_port,
            'dst_port': self._dst_port,
            'size': self._size
        }

    def __repr__(self):
        return (f"FLOW [{self.timestamp}] | proto: {_ip(self.proto)} | "
                f"from {self.src_addr}:{_pp(self.src_port)} via [{self.src_mac}] | "
                f"to {self.dst_addr}:{_pp(self.dst_port)} via [{self.dst_mac}] | "
                f"size: {self.size} | rate: {self.sampling_rate}")
