from .sflow_sample import SFlowSample
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
        print(f"unrecognized flow record: {rformat}")
        upx.unpack_fopaque(length)
        return None

class FlowSample(SFlowSample):

    def __init__(self, sformat, length, sequence_number, source, sampling_rate, sample_pool, drops, input_id, output_id, records_count, records):
        super().__init__(sformat, length)
        self._sequence_number = sequence_number
        self._source = source
        self._sampling_rate = sampling_rate
        self._sample_pool = sample_pool
        self._drops = drops
        self._input_id = input_id
        self._output_id = output_id
        self._records_count = records_count
        self._records = records

    @property
    def sequence_number(self):
        return self._sequence_number

    @property
    def source(self):
        return self._source

    @property
    def sampling_rate(self):
        return self._sampling_rate

    @property
    def sample_pool(self):
        return self._sample_pool

    @property
    def drops(self):
        return self._drops

    @property
    def input_id(self):
        return self._input_id

    @property
    def output_id(self):
        return self._output_id

    @property
    def records_count(self):
        return self._records_count

    @property
    def records(self):
        return self._records

    @classmethod
    def unpack(cls, sformat, length, upx: xdrlib.Unpacker):
        seq_no = upx.unpack_uint()
        source = upx.unpack_uint()
        sampling_rate = upx.unpack_uint()
        sample_pool = upx.unpack_uint()
        drops = upx.unpack_uint()
        input_id = upx.unpack_uint()
        output_id = upx.unpack_uint()
        records_count = upx.unpack_uint()
        if records_count is None:
            records_count = 0
        records = []
        for _ in range(records_count):
            record = create_flow_record(upx)
            if record is not None:
                records.append(record)
        return cls(sformat, length, seq_no, source, sampling_rate,
                   sample_pool, drops, input_id, output_id, records_count, records)

    def __repr__(self):
        return f"""
                    Class: {self.__class__.__name__}
                    Seq.No.: {self.sequence_number}
                    Drops: {self.drops}
                    Records: {self.records}
        """