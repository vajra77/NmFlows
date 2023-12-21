from nmflows.parser.samples import PktHeaderRecord
from datetime import datetime


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

    def __init__(self, ts, rate, vlan, proto, src_mac, dst_mac, src_ip, dst_ip, src_port, dst_port, orig_len, pay_len):
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
        self._original_length = orig_len
        self._payload_length = pay_len

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
    def original_length(self):
        return self._original_length
    
    @property
    def payload_length(self):
        return self._payload_length
    
    @property
    def sampling_rate(self):
        return self._sampling_rate

    @property
    def estimated_size(self):
        if self._original_length < self._payload_length:
            return self._payload_length * self._sampling_rate
        else:
            return self._original_length * self._sampling_rate

    @classmethod
    def from_record(cls, rate, record: PktHeaderRecord):
        return cls(
            datetime.now(),
            rate,
            record.datalink.vlan,
            record.datalink.ether_type,
            record.datalink.source_mac,
            record.datalink.destination_mac,
            record.network.source_address,
            record.network.destination_address,
            record.transport.source_port,
            record.transport.destination_port,
            record.original_length,
            record.network.payload_length
        )

    def __repr__(self):
        return (f"FLOW [{self.timestamp}] | proto: {_ip(self.proto)} | "
                f"from {self.src_addr}:{_pp(self.src_port)} via [{self.src_mac}] | "
                f"to {self.dst_addr}:{_pp(self.dst_port)} via [{self.dst_mac}] | "
                f"original_len: {self.original_length} | payload_len: {self.payload_length} | "
                f"rate: {self.sampling_rate} | computed: {self.estimated_size}")
