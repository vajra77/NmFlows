from nmflows.storage import StorableFlow
from nmflows.utils import MACDirectory
from nmflows.peermatrix.peer_flow import PeerFlow
from datetime import datetime
from elasticsearch import Elasticsearch
from uuid import uuid4


class PeerMatrix:

    def __init__(self, ixf_url):
        self._peers = {}
        self._directory = MACDirectory(ixf_url)

    def dump(self, es_url):
        es = Elasticsearch(es_url)
        for src_peer in self._peers.values():
            for dst_peer in src_peer.destinations():
                flow = {
                    'src_asn': src_peer.asnum,
                    'src_name': src_peer.name,
                    'src_mac': src_peer.mac,
                    'dst_asn': dst_peer.asnum,
                    'dst_name': dst_peer.name,
                    'dst_mac': dst_peer.mac,
                    'ipv4_bytes': dst_peer.ipv4_bytes,
                    'ipv6_bytes': dst_peer.ipv6_bytes,
                    'timestamp': datetime.now()
                }
                es.index(index="nmflows", id=uuid4().hex, document=flow)
        # cleanup matrix
        del self._peers
        self._peers = {}

    def add_flow(self, flow: StorableFlow):
        source = None
        if flow.src_mac in self._peers.keys():
            source = self._peers.get(flow.src_mac)
        else:
            if self._directory.has(flow.src_mac):
                entry = self._directory.get(flow.src_mac)
                source = PeerFlow(entry)
                self._peers[flow.src_mac] = source
        if source is not None:
            dest = None
            if source.exists_destination(flow.dst_mac):
                dest = source.get_destination(flow.dst_mac)
            else:
                if self._directory.has(flow.dst_mac):
                    entry = self._directory.get(flow.dst_mac)
                    dest = PeerFlow(entry)
                    source.add_destination(dest)
            if dest is not None:
                source.account_bytes(flow.computed_size, flow.proto)
                dest.account_bytes(flow.computed_size, flow.proto)
