from nmflows.utils import PtrBuffer, StatLogger
from .exceptions import ParserException
from nmflows.sflow.samples.flow_sample import FlowSample
from nmflows.sflow.samples.expanded_flow_sample import ExpandedFlowSample
import socket


FORMAT_FLOW_SAMPLE = 1
FORMAT_COUNTER_SAMPLE = 2
FORMAT_EXPANDED_FLOW_SAMPLE = 3
FORMAT_EXPANDED_COUNTER_SAMPLE = 4

VALID_SAMPLE_FORMATS = [FORMAT_FLOW_SAMPLE, FORMAT_EXPANDED_FLOW_SAMPLE, FORMAT_COUNTER_SAMPLE, FORMAT_EXPANDED_COUNTER_SAMPLE]

IP_VERSION_4 = 1
IP_VERSION_6 = 2


class SFlowDatagram:

    def __init__(self, version, ip_version, agent_address, agent_id,
                 sequence_number, switch_uptime, samples, skipped):
        self._version = version
        self._ip_version = ip_version
        self._agent_address = agent_address
        self._agent_id = agent_id
        self._sequence_number = sequence_number
        self._switch_uptime = switch_uptime
        self._samples = samples
        self._skipped = skipped

    @property
    def version(self):
        return self._version

    @property
    def ip_version(self):
        if self._ip_version == IP_VERSION_4:
            return 4
        else:
            return 6

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
    def samples_count(self):
        return len(self._samples)

    @property
    def skipped(self):
        return self._skipped

    @property
    def samples(self):
        return self._samples

    @classmethod
    def unpack(cls, version, data: PtrBuffer, stats: StatLogger):
        ip_version = data.read_uint()
        if ip_version == IP_VERSION_4:
            agent_address = socket.inet_ntop(socket.AF_INET, data.read_bytes(4))
        else:
            agent_address = socket.inet_ntop(socket.AF_INET6, data.read_bytes(16))
        agent_id = data.read_uint()
        seq_number = data.read_uint()
        uptime = data.read_uint()
        n_samples = data.read_uint()
        samples = []
        for _ in range(n_samples):
            try:
                sample = cls.create_sflow_sample(data)
                samples.append(sample)
                stats.increment_counter('processed_samples')
            except NotImplementedError:
                stats.increment_counter('not_implemented_samples')
                continue
            except ParserException as e:
                stats.increment_counter('parser_errors')
                stats.debug(e)
                break
        skipped = n_samples - len(samples)
        stats.debug(f"skipped {skipped} samples")
        return cls(version, ip_version, agent_address, agent_id, seq_number, uptime, samples, skipped)

    @staticmethod
    def create_sflow_sample(data: PtrBuffer):
        sformat = data.read_uint() & 0x0fff
        if sformat in VALID_SAMPLE_FORMATS:
            length = data.read_uint()
            if sformat == FORMAT_FLOW_SAMPLE:
                return FlowSample.unpack(sformat, length, data)
            elif sformat == FORMAT_EXPANDED_FLOW_SAMPLE:
                return ExpandedFlowSample.unpack(sformat, length, data)
            elif sformat == FORMAT_COUNTER_SAMPLE or sformat == FORMAT_EXPANDED_COUNTER_SAMPLE:
                data.skip(length - 8)
                raise NotImplementedError
        else:
            raise ParserException(f"unrecognized sample format: {sformat}")

    def __repr__(self):
        return f"""
            Class: {self.__class__.__name__}
            Version: {self.version}
            IP Version: {self.ip_version}
            Agent Address: {self.agent_address}
            Samples No.: {self.samples_count}
            Skipped: {self.skipped}
            Samples: {self.samples}
        """
