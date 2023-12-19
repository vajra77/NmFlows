from nmflows.sflow.samples.flow_record import FlowRecord
from nmflows.sflow.headers.ethernet_frame_header import EthernetFrameHeader
from nmflows.sflow.headers.ipv4_packet_header import IPv4PacketHeader
from nmflows.sflow.headers.ipv6_packet_header import IPv6PacketHeader
from nmflows.sflow.headers.tcp_packet_header import TCPPacketHeader
from nmflows.sflow.headers.udp_packet_header import UDPPacketHeader
from nmflows.sflow.exceptions import ParserException
from nmflows.utils.ptr_buffer import PtrBuffer


PROTO_ETHERNET = 1
PROTO_TCP = 6
PROTO_IPV4 = 11
PROTO_IPV6 = 12
PROTO_UDP = 17

ETHERTYPE_IPV4 = 0x0800
ETHERTYPE_ARP = 0x0806
ETHERTYPE_8021Q = 0x8100
ETHERTYPE_IPV6 = 0x86dd

ALLOWED_ETHERTYPES = [ETHERTYPE_ARP, ETHERTYPE_IPV4, ETHERTYPE_8021Q, ETHERTYPE_IPV6]


class RawPacketHeader(FlowRecord):

    def __init__(self, r_format, length, proto,
                 original_length, stripped, header_length,
                 eth_hdr, ip_hdr, txp_hdr):
        super().__init__(r_format, length)
        self._proto = proto
        self._original_length = original_length
        self._stripped = stripped
        self._header_length = header_length
        self._datalink_header = eth_hdr
        self._network_header = ip_hdr
        self._transport_header = txp_hdr

    @property
    def original_length(self):
        return self._original_length

    @property
    def proto(self):
        return self._proto

    @property
    def payload_length(self):
        result = self._datalink_header.length + \
            self._network_header.length + \
            self._network_header.payload_length
        return result

    @property
    def stripped(self):
        return self._stripped

    @property
    def header_length(self):
        return self._header_length

    @property
    def datalink_header(self):
        return self._datalink_header

    @property
    def network_header(self):
        return self._network_header

    @property
    def transport_header(self):
        return self._transport_header

    @classmethod
    def unpack(cls, rformat, rlength, data: PtrBuffer):
        proto = data.read_uint()
        original_length = data.read_uint()
        stripped = data.read_uint()
        header_length = data.read_uint()
        if proto == PROTO_ETHERNET:
            try:
                header_data = data.read_bytes(header_length)
                ethernet = EthernetFrameHeader.unpack(header_data)

                ip = None
                ip_start = ethernet.length
                if ethernet.type == ETHERTYPE_IPV4:
                    ip = IPv4PacketHeader.unpack(header_data[ip_start:])
                elif ethernet.type == ETHERTYPE_IPV6:
                    ip = IPv6PacketHeader.unpack(header_data[ip_start:])

                txp = None
                txp_start = ethernet.length + ip.length
                if ip.proto == PROTO_TCP:
                    txp = TCPPacketHeader.unpack(header_data[txp_start:])
                elif ip.proto == PROTO_UDP:
                    txp = UDPPacketHeader.unpack(header_data[txp_start:])

                return cls(rformat, rlength, proto, original_length, stripped, header_length, ethernet, ip, txp)
            except ParserException:
                return cls(rformat, rlength, proto, original_length, header_length, None, None, None, None)
        else:
            data.skip(header_length)
            return cls(rformat, rlength, proto, original_length, stripped, header_length, None, None, None)

    def __repr__(self):
        return f"""
                                Class: {self.__class__.__name__}
                                Proto: {self.proto}
                                Original Length: {self.original_length}
                                Stripped: {self.stripped}
                                Payload Length: {self.payload_length}
                                Header Length: {self.header_length}
                                Datalink Header: {self.datalink_header}
                                Network Header: {self.network_header}
                                Transport Header: {self.transport_header}
        """
