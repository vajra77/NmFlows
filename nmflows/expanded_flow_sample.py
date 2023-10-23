from .sflow_sample import SFlowSample
from .ptr_buffer import PtrBuffer


class ExpandedFlowSample(SFlowSample):

    def __init__(self, sformat, length, sequence_number, source_type, source_index,
                 sampling_rate, sample_pool, drops, input_if_format, input_if_value,
                 output_if_format, output_if_value, records_count, records):
        super().__init__(sformat, length)
        super().__init__(sformat, length)
        self._sequence_number = sequence_number
        self._source_type = source_type
        self._source_index = source_index
        self._sampling_rate = sampling_rate
        self._sample_pool = sample_pool
        self._drops = drops
        self._input_if_format = input_if_format
        self._input_if_value = input_if_value
        self._output_if_format = output_if_format
        self._output_if_value = output_if_value
        self._records_count = records_count
        self._records = records

    @property
    def sequence_number(self):
        return self._sequence_number

    @property
    def source_type(self):
        return self._source_type

    @property
    def source_index(self):
        return self._source_index

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
    def input_if_format(self):
        return self._input_if_format

    @property
    def input_if_value(self):
        return self._input_if_value

    @property
    def output_if_format(self):
        return self._output_if_format

    @property
    def output_if_value(self):
        return self._output_if_value

    @property
    def records_count(self):
        return self._records_count

    @property
    def records(self):
        return self._records

    @classmethod
    def unpack(cls, sformat, length, data: PtrBuffer):
        seq_no = data.read_uint()
        source_type = data.read_uint()
        source_index = data.read_uint()
        sampling_rate = data.read_uint()
        sample_pool = data.read_uint()
        drops = data.read_uint()
        input_if_format = data.read_uint()
        input_if_value = data.read_uint()
        output_if_format = data.read_uint()
        output_if_value = data.read_uint()
        records_count = data.read_uint()
        if records_count is None:
            records_count = 0
        records = []
        for _ in range(records_count):
            record = cls.create_flow_record(data)
            if record is not None:
                records.append(record)

        return cls(sformat, length, seq_no, source_type, source_index,
                   sampling_rate, sample_pool, drops,
                   input_if_format, input_if_value,
                   output_if_format, output_if_value,
                   records_count, records)
