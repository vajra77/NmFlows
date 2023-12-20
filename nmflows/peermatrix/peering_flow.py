from nmflows.utils import MACEntry


OVERFLOW = 0xffffffffffffffff


class PeeringFlow:

    def __init__(self, asnum, name, mac):
        self._asnum = asnum
        self._name = name
        self._mac = mac
        self._ipv4_in_bytes = 0
        self._ipv6_in_bytes = 0
        self._ipv4_out_bytes = 0
        self._ipv6_out_bytes = 0
        self._destinations = {}

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
    def destinations(self):
        return self._destinations.values()

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

    def has_destination(self, mac):
        return mac in self._destinations.keys()

    def get_destination(self, mac):
        if mac in self._destinations.keys():
            return self._destinations.get(mac)
        else:
            return PeeringFlow.make_unknown(mac)

    def add_destination(self, peer):
        self._destinations[peer.mac] = peer

    def account_in_bytes(self, size, proto):
        if int(proto) == 2048:
            self._ipv4_in_bytes += size
            if self._ipv4_in_bytes >= OVERFLOW:
                self._ipv4_in_bytes -= OVERFLOW
        else:
            self._ipv6_in_bytes += size
            if self._ipv6_in_bytes >= OVERFLOW:
                self._ipv6_in_bytes -= OVERFLOW

    def account_out_bytes(self, size, proto):
        if int(proto) == 2048:
            self._ipv4_out_bytes += size
            if self._ipv4_out_bytes >= OVERFLOW:
                self._ipv4_out_bytes -= OVERFLOW
        else:
            self._ipv6_out_bytes += size
            if self._ipv6_out_bytes >= OVERFLOW:
                self._ipv6_out_bytes -= OVERFLOW

    def is_unknown(self) -> bool:
        return self._asnum is None and self._name is None

    def is_source(self) -> bool:
        return len(self._destinations) > 0

    def is_destination(self) -> bool:
        return len(self._destinations) == 0

    def cleanup(self):
        self._ipv6_in_bytes = 0
        self._ipv4_in_bytes = 0
        self._ipv6_out_bytes = 0
        self._ipv4_out_bytes = 0
        for p in self._destinations.values():
            p.cleanup()

    @classmethod
    def from_mac_entry(cls, entry: MACEntry):
        return cls(entry.asnum, entry.name, entry.mac)

    @classmethod
    def make_unknown(cls, mac):
        return cls(None, None, mac)
