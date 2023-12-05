from nmflows.utils import MACEntry


class PeerFlow:

    def __init__(self, entry: MACEntry):
        self._asnum = entry.asnum
        self._name = entry.name
        self._mac = entry.mac
        self._ipv4_bytes = 0
        self._ipv6_bytes = 0
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
    def ipv4_bytes(self):
        return self._ipv4_bytes

    @property
    def ipv6_bytes(self):
        return self._ipv6_bytes

    @property
    def bytes(self):
        return self._ipv4_bytes + self._ipv6_bytes

    def exists_destination(self, key):
        return key in self._destinations.keys()

    def get_destination(self, key):
        return self._destinations.get(key)

    def add_destination(self, peer):
        self._destinations[peer.mac] = peer

    def account_bytes(self, size, proto):
        if proto == 4:
            self._ipv4_bytes += size
        else:
            self._ipv6_bytes += size

    def __hash__(self):
        return self._mac
