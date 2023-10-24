from nmflows.sflow.raw_packet_header import RawPacketHeader


class StorableFlow:

    def __init__(self, vlan, proto, src_mac, dst_mac, src_ip, dst_ip, src_port, dst_port, size):
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

    @classmethod
    def from_packet(cls, packet: RawPacketHeader):
        return cls(
            packet.datalink_header.vlan,
            packet.datalink_header.type,
            packet.datalink_header.src_mac,
            packet.datalink_header.dst_mac,
            packet.network_header.src_addr,
            packet.network_header.dst_addr,
            packet.transport_header.src_port,
            packet.transport_header.dst_port,
            packet.payload_length
        )

    def __repr__(self):
        return (f"FLOW: vlan: {self.vlan}, proto: {self.proto} | "
                f"from {self.src_addr}:{self.src_port} via [{self.src_mac}] | "
                f"to {self.dst_addr}:{self.dst_port} via [{self.dst_mac}] | "
                f"size: {self.size}")
