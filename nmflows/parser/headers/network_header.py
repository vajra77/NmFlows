from .ethernet_header import EthernetHeader
from nmflows.utils import Buffer


class NetworkHeader:

    UPPER_PROTO_TCP = 0x06
    UPPER_PROTO_UDP = 0x11

    def __init__(self, version, header_len, total_len, upper_proto, src_addr, dst_addr):
        self._version = version
        self._length = header_len
        self._payload_length = total_len - header_len
        self._upper_proto = upper_proto
        self._source_address = src_addr
        self._destination_address = dst_addr

    @property
    def version(self):
        return self._version

    @property
    def length(self):
        return self._length

    @property
    def payload_length(self):
        return self._payload_length

    @property
    def upper_proto(self):
        return self._upper_proto

    @property
    def source_address(self):
        return self._source_address

    @property
    def destination_address(self):
        return self._destination_address

    @classmethod
    def from_bytes(cls, data, ether_type):
        buffer = Buffer.from_bytes(data)
        if ether_type == EthernetHeader.ETHERTYPE_IPV4:
            # ---- IPv4 Packet Header
            hdr_len = 4 * (buffer.read_byte(0) & 0xf)  # IHL field
            assert hdr_len == 20, "non_default_ipv4_header"
            tot_len = buffer.read_short(2)
            up_proto = buffer.read_byte(9)
            src_addr = buffer.read_ipv4_address(12)
            dst_addr = buffer.read_ipv4_address(16)
            return cls(4, hdr_len, tot_len, up_proto,
                       src_addr, dst_addr)
        elif ether_type == EthernetHeader.ETHERTYPE_IPV6:
            # ---- IPv6 Packet Header
            payload_len = buffer.read_short(4)
            up_proto = buffer.read_byte(6)
            src_addr = buffer.read_ipv6_address(8)
            dst_addr = buffer.read_ipv6_address(24)
            return cls(6, 40, 40 + payload_len, up_proto, src_addr, dst_addr)
        else:
            raise NotImplementedError('non_ip_network_header')
