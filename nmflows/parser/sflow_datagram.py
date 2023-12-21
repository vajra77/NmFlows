from nmflows.utils.buffer import Buffer
from nmflows.utils.stats import StatLogger
from nmflows.parser.samples.sample import Sample
from nmflows.parser.samples.flow_sample import FlowSample
from nmflows.parser.samples.ext_flow_sample import ExtFlowSample


class SFlowDatagram:

    def __init__(self, version, ip_version, ag_address, ag_id, seq_no, uptime, samples):
        self._version = version
        self._ip_version = ip_version
        self._agent_address = ag_address
        self._agent_id = ag_id
        self._sequence_number = seq_no
        self._switch_uptime = uptime
        self._samples = samples

    @property
    def version(self):
        return self._version

    @property
    def ip_version(self):
        return self._ip_version

    @property
    def agent_address(self):
        return self._agent_address

    @property
    def agent_id(self):
        return self._agent_id

    @property
    def sequence_number(self):
        return self._sequence_number

    @property
    def switch_uptime(self):
        return self._switch_uptime

    @property
    def samples(self):
        return self._samples

    @classmethod
    def from_bytes(cls, data, stats: StatLogger):
        buffer = Buffer.from_bytes(data)
        version = buffer.read_uint(0)
        ip_version = buffer.read_uint(4)

        if ip_version == 1:
            agent_address = buffer.read_ipv4_address(8)
            agent_id = buffer.read_uint(12)
            sequence_number = buffer.read_uint(16)
            switch_uptime = buffer.read_uint(20)
            n_samples = buffer.read_uint(24)
            start_of_sample = 28
        else:
            agent_address = buffer.read_ipv6_address(8)
            agent_id = buffer.read_uint(24)
            sequence_number = buffer.read_uint(28)
            switch_uptime = buffer.read_uint(32)
            n_samples = buffer.read_uint(36)
            start_of_sample = 40

        samples = []

        for _ in range(n_samples):
            sample_format = buffer.read_uint(start_of_sample) & 0xfff                          # rightmost 12 bits
            sample_length = buffer.read_uint(start_of_sample + 4)
            if sample_format == Sample.FORMAT_FLOW_SAMPLE:
                sample = FlowSample.from_bytes(sample_format,
                                               sample_length,
                                               buffer.read_bytes(start_of_sample + 8, sample_length), stats)
                samples.append(sample)
                stats.increment_counter('flow_samples')
            elif sample_format == Sample.FORMAT_EXT_FLOW_SAMPLE:
                sample = ExtFlowSample.from_bytes(sample_format,
                                                  sample_length,
                                                  buffer.read_bytes(start_of_sample + 8, sample_length), stats)
                samples.append(sample)
                stats.increment_counter('extended_flow_samples')
            elif sample_format == Sample.FORMAT_COUNTER_SAMPLE:
                stats.increment_counter('counter_samples')
            elif sample_format == Sample.FORMAT_EXT_COUNTER_SAMPLE:
                stats.increment_counter('extended_counter_samples')
            else:
                stats.increment_counter('unknown_samples')
            start_of_sample += 8 + sample_length                        # we assume we can always trust the length field

        return cls(version, ip_version, agent_address, agent_id,
                   sequence_number, switch_uptime, samples)
