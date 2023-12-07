from nmflows.storage import StorableFlow
from nmflows.utils import MACDirectory
from nmflows.peermatrix.peering_flow import PeeringFlow
from datetime import datetime
from elasticsearch import Elasticsearch
from uuid import uuid4


class PeeringMatrix:

    def __init__(self, ixf_url, es_url):
        self._sources = {}
        self._directory = MACDirectory(ixf_url)
        self._log = []
        self._es = Elasticsearch(es_url)
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

    def _checkin_source(self, flow: StorableFlow) -> PeeringFlow:
        source = self.get_source(flow.src_mac)
        if source is None:
            entry = self._directory.get(flow.src_mac)
            if entry is not None:
                source = PeeringFlow.from_mac_entry(entry)
                self._add_source(source)
            else:
                source = PeeringFlow.make_unknown(flow.src_mac)
        return source

    def _checkin_destination(self, flow: StorableFlow) -> PeeringFlow:
        source = self._checkin_source(flow)
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

    def add_flow(self, flow: StorableFlow):
        self._is_dirty = True
        source = self._checkin_source(flow)
        dest = self._checkin_destination(flow)
        if source.is_unknown() or dest.is_unknown():
            self._do_log(f"source/dest unknown: [{flow.src_mac}/{flow.dst_mac}]")
            return
        else:
            source.account_bytes(flow.computed_size, flow.proto)
            dest.account_bytes(flow.computed_size, flow.proto)

    def flush(self):
        try:
            if self.is_dirty:
                for src in self._sources.values():
                    for dst in src.destinations:
                        flow = {
                            'src_asn': src.asnum,
                            'src_name': src.name,
                            'src_mac': src.mac,
                            'dst_asn': dst.asnum,
                            'dst_name': dst.name,
                            'dst_mac': dst.mac,
                            'ipv4_bytes': dst.ipv4_bytes,
                            'ipv6_bytes': dst.ipv6_bytes,
                            'timestamp': datetime.now()
                        }
                        self._es.index(index="nmflows", id=uuid4().hex, document=flow)
                    src.cleanup()
                self._is_dirty = False
        except Exception as e:
            print(f"Error while dumping to ES: {e}")

    def dump(self, filename):
        with open(filename, 'w+') as f:
            f.write(str(self))

    def _do_log(self, msg):
        timestamp = datetime.now()
        self._log.append(f"{timestamp}: {msg}")

    def __repr__(self):
        msg = ""
        for src in self._sources.values():
            msg += f"FROM: {src.name}[{src.mac}] TO: "
            tot4 = 0
            tot6 = 0
            for dst in src.destinations:
                msg += f"{dst.name}[{dst.mac}]=({dst.ipv4_bytes}/{dst.ipv6_bytes}) "
                tot4 += dst.ipv4_bytes
                tot6 += dst.ipv6_bytes
            msg += f"| SUM({tot4}/{tot6}) TOT({src.ipv4_bytes}/{src.ipv6_bytes})\n"
        return msg    
