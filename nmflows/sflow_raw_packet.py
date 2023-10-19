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

    @classmethod
    def unpack(cls, data):
        upx = xdrlib.Unpacker(data)
        version = upx.unpack_uint()
        ip_version = upx.unpack_uint()
        if ip_version == IP_VERSION_4:
            agent_address = socket.inet_ntop(socket.AF_INET, upx.unpack_fopaque(4))
        else:
            agent_address = socket.inet_ntop(socket.AF_INET6, upx.unpack_fopaque(16))
        agent_id = upx.unpack_uint()
        seq_number = upx.unpack_uint()
        uptime = upx.unpack_uint()
        n_samples = upx.unpack_uint()
        samples = upx.unpack_bytes()
        upx.done()
        return cls(version, ip_version, agent_address, agent_id, seq_number, uptime, n_samples, samples)

