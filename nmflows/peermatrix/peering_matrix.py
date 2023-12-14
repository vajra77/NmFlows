from nmflows.storage import StorableFlow
from nmflows.utils import MACDirectory
from nmflows.peermatrix.peering_flow import PeeringFlow
from nmflows.backend import Backend


class PeeringMatrix:

    def __init__(self, directory: MACDirectory, backend: Backend):
        self._sources = {}
        self._directory = directory
        self._backend = backend
        self._is_dirty = False

    @property
    def is_dirty(self) -> bool:
        return self._is_dirty

    def has_source(self, mac):
        return mac in self._sources.keys()

    def get_source(self, mac):
        if self.has_source(mac):
            return self._sources[mac]
        else:
            return None

    def _add_source(self, source):
        self._sources[source.mac] = source

    def _get_flow_source(self, flow: StorableFlow) -> PeeringFlow:
        source = self.get_source(flow.src_mac)
        if source is None:
            entry = self._directory.get(flow.src_mac)
            if entry is not None:
                source = PeeringFlow.from_mac_entry(entry)
                self._add_source(source)
            else:
                source = PeeringFlow.make_unknown(flow.src_mac)
        return source

    def _get_flow_destination(self, flow: StorableFlow) -> PeeringFlow:
        source = self._get_flow_source(flow)
        if source.is_unknown():
            dest = PeeringFlow.make_unknown(flow.dst_mac)
        else:
            dest = source.get_destination(flow.dst_mac)
            if dest.is_unknown():
                entry = self._directory.get(flow.dst_mac)
                if entry is not None:
                    dest = PeeringFlow.from_mac_entry(entry)
                    source.add_destination(dest)
        return dest

    def _get_flow_destination_as_source(self, flow: StorableFlow) -> PeeringFlow:
        das = self.get_source(flow.dst_mac)
        if das is None:
            entry = self._directory.get(flow.dst_mac)
            if entry is not None:                                                                                       # This should always be true at the point method is called
                das = PeeringFlow.from_mac_entry(entry)
                self._add_source(das)
        return das

    def add_flow(self, flow: StorableFlow):
        source = self._get_flow_source(flow)
        dest = self._get_flow_destination(flow)
        if source.is_unknown() or dest.is_unknown():
            return
        else:
            source.account_out_bytes(flow.computed_size, flow.proto)
            dest.account_in_bytes(flow.computed_size, flow.proto)
            dest_as_source = self._get_flow_destination_as_source(flow)
            dest_as_source.account_in_bytes(flow.computed_size, flow.proto)
            self._is_dirty = True

    def flush(self):
        if self.is_dirty:
            for src in self._sources.values():
                self._backend.store_peer(src)
                self._backend.store_flows(src)
                src.cleanup()
            self._is_dirty = False

    def dump(self, filename):
        with open(filename, 'w+') as f:
            f.write(str(self))

    def __repr__(self):
        msg = ""
        for src in self._sources.values():
            msg += f"FROM: {src.name}[{src.mac}] TO: "
            tot4 = 0
            tot6 = 0
            for dst in src.destinations:
                # msg += f"{dst.name}[{dst.mac}]=({dst.ipv4_in_bytes}/{dst.ipv6_in_bytes}) "
                msg += f"{dst.name}[{dst.mac}], "
                tot4 += dst.ipv4_in_bytes
                tot6 += dst.ipv6_in_bytes
            # msg += f"| SUM({tot4}/{tot6}) TOT({src.ipv4_out_bytes}/{src.ipv6_out_bytes})\n"
        return msg    
