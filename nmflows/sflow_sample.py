from .raw_packet_header import RawPacketHeader
from .exceptions import ParserException
from .ptr_buffer import PtrBuffer


FORMAT_FLOW_SAMPLE = 1
FORMAT_COUNTER_SAMPLE = 2
FORMAT_EXPANDED_FLOW_SAMPLE = 3

RECORD_RAW_HEADER = 1
RECORD_ETHERNET_DATA = 2
RECORD_IPV4_DATA = 3
RECORD_IPV6_DATA = 4


class SFlowSample:

    def __init__(self, sformat, length):
        self._format = sformat
        self._length = length

    @property
    def format(self):
        return self._format

    @property
    def length(self):
        return self._length

    def is_flow_sample(self):
        return self._format == FORMAT_FLOW_SAMPLE

    def is_counter_sample(self):
        return self._format == FORMAT_COUNTER_SAMPLE

    def is_expanded_flow_sample(self):
        return self._format == FORMAT_EXPANDED_FLOW_SAMPLE

    @classmethod
    def unpack(cls, sformat, length, data: PtrBuffer):
        raise NotImplementedError

    @staticmethod
    def create_flow_record(data: PtrBuffer):
        rformat = data.read_uint()
        length = data.read_uint()
        if rformat == RECORD_RAW_HEADER:
            return RawPacketHeader.unpack(rformat, length, data)
        elif rformat == RECORD_ETHERNET_DATA:
            data.read_bytes(length)
            raise ParserException(f"unhandled Ethernet Data Record")
        else:
            data.read_bytes(length)
            raise ParserException(f"unrecognized flow record type")
