from nmflows.utils.buffer import Buffer
from nmflows.utils.stats import StatLogger
from .sample import Sample
from .flow_sample import FlowSample
from .record import Record
from .pkt_header_record import PktHeaderRecord


class ExtFlowSample(FlowSample):

    def __init__(self, sformat, length, seq_no, src_id, sampling_rate,
                 sample_pool, drops, input_iface, output_iface, records):
        assert sformat == Sample.FORMAT_EXT_FLOW_SAMPLE
        super().__init__(sformat, length, seq_no, src_id, sampling_rate,
                 sample_pool, drops, input_iface, output_iface, records)

    @classmethod
    def from_bytes(cls, sformat, length, data, stats: StatLogger):
        buffer = Buffer.from_bytes(data)
        seq_no = buffer.read_uint(0)
        src_id = buffer.read_uint(4)
        sampling_rate = buffer.read_uint(12)
        sample_pool = buffer.read_uint(16)
        drops = buffer.read_uint(20)
        input_iface = buffer.read_uint(28)                  # we don't mind exact format
        output_iface = buffer.read_uint(36)
        number_of_records = buffer.read_uint(40)
        start_of_record = 44
        records = []

        for _ in range(number_of_records):
            record_format = buffer.read_uint(start_of_record)
            record_length = buffer.read_uint(start_of_record + 4)
            try:
                if record_format == Record.FORMAT_RAW_PACKET:
                    record = PktHeaderRecord.from_bytes(record_format, record_length,
                                                        buffer.read_bytes(start_of_record + 8, record_length))
                    records.append(record)
                else:
                    stats.increment_counter('non_packet_header_record')
            except NotImplementedError as e:
                stats.debug(e)
                stats.increment_counter('unrecognized_data_in_record')
            finally:
                start_of_record += 8 + record_length                                   # we always trust the length data

        return cls(sformat, length, seq_no, src_id, sampling_rate,
                   sample_pool, drops, input_iface, output_iface, records)
