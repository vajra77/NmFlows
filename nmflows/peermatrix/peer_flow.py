

class PeerFlow:

    def __init__(self, code, src_mac):
        self._code = code
        self._mac = src_mac
        self._ipv4_bytes = 0
        self._ipv6_bytes = 0
        self._destinations = {}

    @property
    def code(self):
        return self._code

    @property
    def mac(self):
        return hash(self._mac)

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

    def __hash__(self):
        return self._mac
