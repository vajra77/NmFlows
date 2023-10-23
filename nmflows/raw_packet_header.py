from .flow_record import FlowRecord
from .ethernet_frame_header import EthernetFrameHeader
from .ipv4_packet_header import IPv4PacketHeader
from .exceptions import ParserException
import xdrlib


PROTO_ETHERNET = 1
PROTO_IPV4 = 11
PROTO_IPV6 = 12

ETHERTYPE_IPV4 = 0x0800
ETHERTYPE_ARP = 0x0806
ETHERTYPE_8021Q = 0x8100
ETHERTYPE_IPV6 = 0x86dd

ALLOWED_ETHERTYPES = [ ETHERTYPE_ARP, ETHERTYPE_IPV4, ETHERTYPE_8021Q, ETHERTYPE_IPV6]

class RawPacketHeader(FlowRecord):

    def __init__(self, r_format, length, proto, payload_length, stripped, header_length, eth_hdr, ip_hdr, txp_hdr):
        super().__init__(r_format, length)
        self._proto = proto
        self._payload_length = payload_length
        self._stripped = stripped
        self._header_length = header_length
        self._datalink_header = eth_hdr
        self._network_header = ip_hdr
        self._transport_header = txp_hdr

    @property
    def proto(self):
        return self._proto

    @property
    def payload_length(self):
        return self._payload_length

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
    def unpack(cls, rformat, rlength, upx: xdrlib.Unpacker):
        proto = upx.unpack_uint()
        length = upx.unpack_uint()
        stripped = upx.unpack_uint()
        header_length = upx.unpack_uint()
        position = upx.get_position()
        if proto == PROTO_ETHERNET:
            try:
                ethernet = EthernetFrameHeader.unpack(upx)
                if ethernet.type == ETHERTYPE_IPV4:
                    ip = IPv4PacketHeader.unpack(upx)
                    upx.unpack_fopaque(header_length - ethernet.length - ip.length)
                else:
                    ip = None
                    upx.unpack_fopaque(header_length - ethernet.length)
            except ParserException:
                print("error while parsing eth/ip")
                upx.set_position(position)
                upx.unpack_fopaque(header_length)
                return cls(rformat, rlength, proto, length, stripped, header_length, None, None, None)
            else:
                return cls(rformat, rlength, proto, length, stripped, header_length, ethernet, ip, None)
        else:
            upx.unpack_fopaque(header_length)
            return cls(rformat, rlength, proto, length, stripped, header_length, None, None, None)

    def __repr__(self):
        return f"""
                                Class: {self.__class__.__name__}
                                Proto: {self.proto}
                                Length: {self.length}
                                Payload Length: {self.payload_length}
                                Stripped: {self.stripped}
                                Header Length: {self.header_length}
                                Datalink Header: {self.datalink_header}
                                Network Header: {self.network_header}
                                Transport Header: {self.transport_header}
        """