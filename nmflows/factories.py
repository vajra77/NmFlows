from .raw_packet_header import RawPacketHeader
from .flow_sample import FlowSample
import xdrlib

FORMAT_FLOW_SAMPLE = 1
FORMAT_COUNTER_SAMPLE = 2

RECORD_RAW_HEADER = 1
RECORD_ETHERNET_DATA = 2
RECORD_IPV4_DATA = 3
RECORD_IPV6_DATA = 4


def create_sflow_sample(upx: xdrlib.Unpacker):
    sformat = upx.unpack_uint()
    length = upx.unpack_uint()
    if sformat == FORMAT_FLOW_SAMPLE:
        return FlowSample.unpack(sformat, length, upx)
    else:
        upx.unpack_fopaque(length)
        return None

def create_flow_record(upx: xdrlib.Unpacker):
    rformat = upx.unpack_uint()
    length = upx.unpack_uint()
    if rformat == RECORD_RAW_HEADER:
        return RawPacketHeader.unpack(rformat, length, upx)
    else:
        upx.unpack_fopaque(length)
        return None

