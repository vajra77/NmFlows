from .record import Record

class RawPacketHeader(Record):

    def __init__(self, rformat, length):
        assert rformat == Record.FORMAT_RAW_PACKET
        super().__init__(rformat, length)

    @classmethod
    def from_bytes(cls, rformat, length, data):
        pass
