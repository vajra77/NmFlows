from nmflows.utils import MACDirectory, StorableFlow
from nmflows.peermatrix.peer_flow import PeerFlow
from nmflows.backend.backend import Backend
from pprint import pprint


class PeeringMatrix:

    def __init__(self, directory: MACDirectory, backend: Backend):
        self._peers = {}
        self._directory = directory
        self._backend = backend
        self._is_dirty = False

    @property
    def is_dirty(self) -> bool:
        return self._is_dirty

    def _has_peer(self, mac):
        return mac in self._peers.keys()
    
    def _get_peer(self, mac) -> PeerFlow:
        if self._has_peer(mac):
            return self._peers[mac]
        else:
            return PeerFlow.make_unknown(mac)

    def checkin_peer(self, mac) -> PeerFlow:
        peer = self._peers.get(mac)
        if peer is not None:
            return peer
        else:
            mac_entry = self._directory.get(mac)
            if mac_entry is not None:
                peer = PeerFlow.from_mac_entry(mac_entry)
                self._peers[mac] = peer
                return peer
            else:
                return PeerFlow.make_unknown(mac)

    def checkin_flow(self, peer: PeerFlow, mac: str) -> PeerFlow:
        flow_dst = peer.get_flow(mac)
        if flow_dst is not None:
            return flow_dst
        else:
            mac_entry = self._directory.get(mac)
            if mac_entry is not None:
                flow_dst = PeerFlow.from_mac_entry(mac_entry)
                peer.add_flow(flow_dst)
                return flow_dst
            else:
                return PeerFlow.make_unknown(mac)

    def register_flow(self, flow: StorableFlow):

        src = self.checkin_peer(flow.src_mac)
        dst = self.checkin_peer(flow.dst_mac)

        pprint(src)

        if not src.is_unknown():
            src.account_in_bytes(flow.estimated_size, flow.proto)
            self._is_dirty = True
            fdest = self.checkin_flow(src, flow.dst_mac)
            if not fdest.is_unknown():
                fdest.account_out_bytes(flow.estimated_size, flow.proto)

        if not dst.is_unknown():
            dst.account_out_bytes(flow.estimated_size, flow.proto)
            self._is_dirty = True

    def flush(self):
        if self.is_dirty:
            for src in self._peers.values():
                self._backend.store_peer(src)
                self._backend.store_flows(src)
                src.cleanup()
            self._is_dirty = False

    def dump(self, filename):
        with open(filename, 'w+') as f:
            f.write(str(self))

    def __repr__(self):
        msg = ""
        for src in self._peers.values():
            msg += f"FROM: {src.name}[:{src.mac[-2:]}] TO: "
            tot4 = 0
            tot6 = 0
            for dst in src.destinations:
                # msg += f"{dst.name}[{dst.mac}]=({dst.ipv4_in_bytes}/{dst.ipv6_in_bytes}) "
                msg += f"{dst.name}[:{dst.mac[-2:]}] | "
                tot4 += dst.ipv4_in_bytes
                tot6 += dst.ipv6_in_bytes
            # msg += f"| SUM({tot4}/{tot6}) TOT({src.ipv4_out_bytes}/{src.ipv6_out_bytes})\n"
            msg += "\n-----------------------------------------------------------\n"
        return msg    
