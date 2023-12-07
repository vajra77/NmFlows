from nmflows.storage import StorableFlow
from nmflows.utils import MACDirectory
from nmflows.peermatrix.peering_flow import PeeringFlow
from datetime import datetime
from elasticsearch import Elasticsearch
from uuid import uuid4


class PeeringMatrix:

    def __init__(self, ixf_url):
        self._sources = {}
        self._directory = MACDirectory(ixf_url)
        self._log = []

    def has_source(self, mac):
        return mac in self._sources.keys()

    def get_source(self, mac):
        if self.has_source(mac):
            return self._sources[mac]
        else:
            return None

    def add_source(self, source):
        self._sources[source.mac] = source

    def _checkin_source(self, flow: StorableFlow) -> PeeringFlow:
        source = self.get_source(flow.src_mac)
        if source is None:
            entry = self._directory.get(flow.src_mac)
            if entry is not None:
                source = PeeringFlow.from_mac_entry(entry)
                self.add_source(source)
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
        source = self._checkin_source(flow)
        dest = self._checkin_destination(flow)
        if source.is_unknown() or dest.is_unknown():
            self._do_log(f"source/dest unknown: [{flow.src_mac}/{flow.dst_mac}]")
            return
        else:
            source.account_bytes(flow.computed_size, flow.proto)
            dest.account_bytes(flow.computed_size, flow.proto)

    def flush(self, es_url):
        try:
            es = Elasticsearch(es_url)
            for src in self._sources.values():
                for dst in src.destinations():
                    pprint(src)
                    pprint(dst)
                #     flow = {
                #         'src_asn': src.asnum,
                #         'src_name': src.name,
                #         'src_mac': src.mac,
                #         'dst_asn': dst.asnum,
                #         'dst_name': dst.name,
                #         'dst_mac': dst.mac,
                #         'ipv4_bytes': dst.ipv4_bytes,
                #         'ipv6_bytes': dst.ipv6_bytes,
                #         'timestamp': datetime.now()
                #     }
                #     es.index(index="nmflows", id=uuid4().hex, document=flow)
                # src.cleanup()
        except Exception as e:
            print(f"Error while dumping to ES: {e}")

    def _do_log(self, msg):
        timestamp = datetime.now()
        self._log.append(f"{timestamp}: {msg}")
