from .ethernet_frame_data import EthernetFrameData
from .raw_packet_header import RawFrameHeader
import xdrlib




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

    @classmethod
    def unpack(cls, upx: xdrlib.Unpacker):
        pass
