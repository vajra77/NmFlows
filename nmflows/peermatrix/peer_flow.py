

class PeerFlow:

    def __init__(self, src_mac):
        self._mac = src_mac
        self._ipv4_in_bytes = 0
        self._ipv6_in_bytes = 0
        self._ipv4_out_bytes = 0
        self._ipv6_out_bytes = 0
        self._peers = {}

    @property
    def mac(self):
        return hash(self._mac)

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

    def exists_destination(self, peer):
        return peer in self._peers.keys()

    def get_destination(self, peer):
        return self._peers.get(peer)

    def add_destination(self, peer):
        self._peers[peer] = peer

    def __hash__(self):
        return self._mac
