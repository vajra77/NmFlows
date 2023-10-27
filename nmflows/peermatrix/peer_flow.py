

class PeerFlow:

    def __init__(self, code, src_mac):
        self._code = code
        self._mac = src_mac
        self._ipv4_in_bytes = 0
        self._ipv6_in_bytes = 0
        self._ipv4_out_bytes = 0
        self._ipv6_out_bytes = 0
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
    def ipv4_in_bytes(self):
        return self._ipv4_in_bytes

    @property
    def ipv6_in_bytes(self):
        return self._ipv6_in_bytes

    @property
    def ipv4_out_bytes(self):
        return self._ipv4_out_bytes

    @property
    def ipv6_out_bytes(self):
        return self._ipv6_out_bytes

    @property
    def in_bytes(self):
        return self._ipv4_in_bytes + self._ipv6_in_bytes

    @property
    def out_bytes(self):
        return self._ipv4_out_bytes + self._ipv6_out_bytes

    def exists_destination(self, key):
        return key in self._destinations.keys()

    def get_destination(self, key):
        return self._destinations.get(key)

    def add_destination(self, peer):
        self._destinations[peer.mac] = peer

    def __hash__(self):
        return self._mac
