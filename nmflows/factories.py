from .raw_packet_header import RawPacketHeader
import xdrlib


FORMAT_RAW_HEADER = 1
FORMAT_ETHERNET_DATA = 2
FORMAT_IPV4_DATA = 3
FORMAT_IPV6_DATA = 4


def create_flow_record(upx: xdrlib.Unpacker):
    rformat = upx.unpack_uint()
    length = upx.unpack_uint()
    if rformat == FORMAT_RAW_HEADER:
        return RawPacketHeader.unpack(rformat, length, upx)
    else:
        upx.unpack_fopaque(length)
        return None