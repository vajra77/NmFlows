from nmflows.utils.buffer import Buffer
from nmflows.utils.stats import StatLogger
from .sample import Sample
from .record import Record
from .pkt_header_record import PktHeaderRecord


class FlowSample(Sample):

    def __init__(self, sformat, length, seq_no, src_id, sampling_rate,
                 sample_pool, drops, input_iface, output_iface, records):
        assert sformat == Sample.FORMAT_FLOW_SAMPLE
        super().__init__(sformat, length)
        self._sequence_number = seq_no
        self._source_id = src_id
        self._sampling_rate = sampling_rate
        self._sample_pool = sample_pool
        self._drops = drops
        self._input_iface = input_iface
        self._output_iface = output_iface
        self._records = records

    @property
    def sequence_number(self):
        return self._sequence_number

    @property
    def source_id(self):
        return self._source_id

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
    def input_iface(self):
        return self._input_iface

    @property
    def output_iface(self):
        return self._output_iface

    @property
    def records(self):
        return self._records

    @property
    def number_of_records(self):
        return len(self._records)

    @classmethod
    def from_bytes(cls, sformat, length, data, stats: StatLogger):
        buffer = Buffer.from_bytes(data)
        seq_no = buffer.read_uint(0)
        src_id = buffer.read_uint(4)
        sampling_rate = buffer.read_uint(8)
        sample_pool = buffer.read_uint(12)
        drops = buffer.read_uint(16)
        input_iface = buffer.read_uint(20)
        output_iface = buffer.read_uint(24)
        number_of_records = buffer.read_uint(28)
        start_of_record = 32
        records = []

        for _ in range(number_of_records):
            record_format = buffer.read_uint(start_of_record)
            record_length = buffer.read_uint(start_of_record + 4)
            try:
                if record_format == Record.FORMAT_RAW_PACKET:
                    record = PktHeaderRecord.from_bytes(record_format, record_length,
                                                        buffer.read_bytes(start_of_record + 8, record_length))
                    records.append(record)
                    stats.increment_counter('raw_packet_header_record')
                else:
                    stats.increment_counter('non_packeet_header_record')
            except NotImplementedError as e:
                stats.increment_counter(e)
                stats.increment_counter('unrecognized_data_in_record')
            finally:
                start_of_record += 8 + record_length                                   # we always trust the length data

        return cls(sformat, length, seq_no, src_id, sampling_rate,
                   sample_pool, drops, input_iface, output_iface, records)
