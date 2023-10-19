import xdrlib
import socket

IP_VERSION_4 = 1
IP_VERSION_6 = 2

class SFlowRawPacket:

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

    @classmethod
    def unpack(cls, data):
        upx = xdrlib.Unpacker(data)
        version = upx.unpack_uint()
        if version != 5:
            raise Exception(f"sFlow version not supported: v{version}")
        ip_version = upx.unpack_uint()
        if ip_version == IP_VERSION_4:
            agent_address = socket.inet_pton(socket.AF_INET, upx.unpack_fopaque(4))
        else:
            agent_address = socket.inet_ntop(socket.AF_INET6, upx.unpack_fopaque(16))
        agent_id = upx.unpack_uint()
        seq_number = upx.unpack_uint()
        uptime = upx.unpack_uint()
        n_samples = upx.unpack_uint()
        samples = upx.unpack_bytes()
        # upx.done()
        return cls(version, ip_version, agent_address, agent_id, seq_number, uptime, n_samples, samples)

    def __repr__(self):
        rep = f"""
            Class: {self.__class__.__name__}
            Version: {self.version}
            IP Version: {self.ip_version}
            Agent Address: {self.agent_address}
            Samples No.: {self.samples_count}
        """
        return rep
