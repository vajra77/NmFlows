from nmflows.storage import StorableFlow
from .peer_flow import PeerFlow


class PeerMatrix:

    def __init__(self):
        self._peers = {}
        self._locked = False

    @property
    def locked(self):
        return self._locked

    def lock(self):
        self._locked = True

    def unlock(self):
        self._locked = False

    def dump(self):
        pass

    def add_flow(self, flow: StorableFlow):

        if flow.src_mac in self._peers.keys():
            source = self._peers.get(flow.src_mac)
        else:
            source = PeerFlow(flow.src_mac)

        if source.exists_destination(flow.dst_mac):
            dest = source.get_destination(flow.dst_mac)
        else:
            dest = PeerFlow(flow.dst_mac)

        if flow.proto == 4:
            dest.account_ipv4_bytes_in(flow.computed_size)
            source.account_ipv4_bytes_out(flow.computed_size)
        else:
            dest.account_ipv6_bytes_in(flow.computed_size)
            source.account_ipv6_bytes_out(flow.computed_size)
