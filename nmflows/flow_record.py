from .raw_packet_header import RawPacketHeader
import xdrlib


RECORD_RAW_HEADER = 1
RECORD_ETHERNET_DATA = 2
RECORD_IPV4_DATA = 3
RECORD_IPV6_DATA = 4


def create_flow_record(upx: xdrlib.Unpacker):
    rformat = upx.unpack_uint()
    length = upx.unpack_uint()
    if rformat == RECORD_RAW_HEADER:
        return RawPacketHeader.unpack(rformat, length, upx)
    else:
        upx.unpack_fopaque(length)
        return None

class FlowRecord:

    def __init__(self, r_format, length):
        self._format = r_format
        self._length = length

    @property
    def format(self):
        return self._format

    @property
    def length(self):
        return self._length
