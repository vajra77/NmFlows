from .flow_sample import FlowSample
import socket
import xdrlib

FORMAT_FLOW_SAMPLE = 1
FORMAT_COUNTER_SAMPLE = 2
FORMAT_EXPANDED_FLOW_SAMPLE = 3

IP_VERSION_4 = 1
IP_VERSION_6 = 2


def create_sflow_sample(upx: xdrlib.Unpacker):
    sformat = upx.unpack_uint()
    if sformat is None:
        raise Exception("unable to parse sflow sample format")
    length = upx.unpack_uint()
    if length is None:
        raise Exception("unable to parse sflow sample length")
    if sformat == FORMAT_FLOW_SAMPLE:
        return FlowSample.unpack(sformat, length, upx)
    else:
        upx.unpack_fopaque(length)
        raise Exception(f"unrecognized sample format: {sformat}")

class SFlowDatagram:

    def __init__(self, version, ip_version, agent_address, agent_id, sequence_number, switch_uptime, samples_count, samples):
        self._version = version
        self._ip_version = ip_version
        self._agent_address = agent_address
        self._agent_id = agent_id
        self._sequence_number = sequence_number
        self._switch_uptime = switch_uptime
        self._samples_count = samples_count
        self._samples = samples

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
    def switch_uptim(self):
        return self._switch_uptime

    @property
    def samples_count(self):
        return self._samples_count

    @property
    def samples(self):
        return self._samples

    @classmethod
    def unpack(cls, version, upx):
        ip_version = upx.unpack_uint()
        if ip_version == IP_VERSION_4:
            agent_address = socket.inet_ntop(socket.AF_INET, upx.unpack_fopaque(4))
        else:
            raise NotImplementedError
            # agent_address = socket.inet_ntop(socket.AF_INET6, upx.unpack_fopaque(16))
        agent_id = upx.unpack_uint()
        seq_number = upx.unpack_uint()
        uptime = upx.unpack_uint()
        n_samples = upx.unpack_uint()
        if n_samples is None:
            n_samples = 0
        samples = []
        for _ in range(n_samples):
            sample = create_sflow_sample(upx)
            samples.append(sample)
        return cls(version, ip_version, agent_address, agent_id, seq_number, uptime, n_samples, samples)

    def __repr__(self):
        return f"""
            Class: {self.__class__.__name__}
            Version: {self.version}
            IP Version: {self.ip_version}
            Agent Address: {self.agent_address}
            Samples No.: {self.samples_count}
            Samples: {self.samples}
        """
