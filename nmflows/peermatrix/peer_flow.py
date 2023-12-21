from nmflows.utils import MACEntry


class PeerFlow:

    def __init__(self, asnum, name, mac):
        self._asnum = asnum
        self._name = name
        self._mac = mac
        self._ipv4_in_bytes = 0
        self._ipv6_in_bytes = 0
        self._ipv4_out_bytes = 0
        self._ipv6_out_bytes = 0
        self._flows = {}

    @property
    def asnum(self):
        return self._asnum

    @property
    def name(self):
        return self._name

    @property
    def mac(self):
        return self._mac

    @property
    def flows(self):
        return self._flows.values()

    @property
    def ipv4_in_bytes(self):
        return self._ipv4_in_bytes

    @property
    def ipv4_out_bytes(self):
        return self._ipv4_out_bytes

    @property
    def ipv6_in_bytes(self):
        return self._ipv6_in_bytes

    @property
    def ipv6_out_bytes(self):
        return self._ipv6_out_bytes

    @property
    def in_bytes(self):
        return self._ipv4_in_bytes + self._ipv6_in_bytes

    @property
    def out_bytes(self):
        return self._ipv4_out_bytes + self._ipv6_out_bytes

    def has_flow(self, mac):
        return mac in self._flows.keys()

    def get_flow(self, mac):
        if mac in self._flows.keys():
            return self._flows.get(mac)
        else:
            return PeerFlow.make_unknown(mac)

    def add_flow(self, peer):
        self._flows[peer.mac] = peer

    def account_in_bytes(self, size, proto):
        if int(proto) == 2048:
            self._ipv4_in_bytes += size
        else:
            self._ipv6_in_bytes += size

    def account_out_bytes(self, size, proto):
        if int(proto) == 2048:
            self._ipv4_out_bytes += size
        else:
            self._ipv6_out_bytes += size

    def is_unknown(self) -> bool:
        return self._asnum is None and self._name is None

    def cleanup(self):
        self._ipv6_in_bytes = 0
        self._ipv4_in_bytes = 0
        self._ipv6_out_bytes = 0
        self._ipv4_out_bytes = 0
        for p in self._flows.values():
            p.cleanup()

    @classmethod
    def from_mac_entry(cls, entry: MACEntry):
        return cls(entry.asnum, entry.name, entry.mac)

    @classmethod
    def make_unknown(cls, mac):
        return cls(None, None, mac)
