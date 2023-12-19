from nmflows.sflow.samples.sflow_sample import SFlowSample
from nmflows.sflow.exceptions import ParserException
from nmflows.utils.ptr_buffer import PtrBuffer


class FlowSample(SFlowSample):

    def __init__(self, sformat, length, sequence_number,
                 source, sampling_rate, sample_pool, drops,
                 input_if, output_if, records):
        super().__init__(sformat, length)
        self._sequence_number = sequence_number
        self._source = source
        self._sampling_rate = sampling_rate
        self._sample_pool = sample_pool
        self._drops = drops
        self._input_if = input_if
        self._output_if = output_if
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
    def input_if(self):
        return self._input_if

    @property
    def output_if(self):
        return self._output_if

    @property
    def records_count(self):
        return len(self._records)

    @property
    def records(self):
        return self._records

    @classmethod
    def unpack(cls, sformat, length, data: PtrBuffer):
        seq_no = data.read_uint()
        source = data.read_uint()
        sampling_rate = data.read_uint()
        sample_pool = data.read_uint()
        drops = data.read_uint()
        input_if = data.read_uint()
        output_if = data.read_uint()
        records_count = data.read_uint()
        records = []
        for _ in range(records_count):
            try:
                record = cls.create_flow_record(data)
                records.append(record)
            except ParserException:
                break

        return cls(sformat, length, seq_no, source, sampling_rate,
                   sample_pool, drops, input_if, output_if, records)

    def __repr__(self):
        return f"""
                    Class: {self.__class__.__name__}
                    Seq.No.: {self.sequence_number}
                    Drops: {self.drops}
                    Records: {self.records}
        """