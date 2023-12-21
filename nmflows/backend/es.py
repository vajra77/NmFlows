from nmflows.peermatrix.peer_flow import PeerFlow
from .backend import Backend
from elasticsearch import Elasticsearch
from datetime import datetime
from uuid import uuid4

class ESBackend(Backend):

    def __init__(self, es_url, index):
        self._url = es_url
        self._index = index
        self._es = Elasticsearch(es_url)

    def store_flows(self, src: PeerFlow):
        for dst in src.destinations:
            flow = {
                'timestamp': datetime.now(),
                'type': 'flow',
                'src_asn': src.asnum,
                'src_name': src.name,
                'src_mac': src.mac,
                'dst_asn': dst.asnum,
                'dst_name': dst.name,
                'dst_mac': dst.mac,
                'ipv4_bytes': dst.ipv4_in_bytes,
                'ipv6_bytes': dst.ipv6_in_bytes,
            }
            self._es.index(index=self._index, id=uuid4().hex, document=flow)

    def store_peer(self, src: PeerFlow):
        peer = {
            'timestamp': datetime.now(),
            'type': 'peer',
            'asn': src.asnum,
            'name': src.name,
            'mac': src.mac,
            'ipv4_in_bytes': src.ipv4_in_bytes,
            'ipv4_out_bytes': src.ipv4_out_bytes,
            'ipv6_in_bytes': src.ipv6_in_bytes,
            'ipv6_out_bytes': src.ipv6_out_bytes,
            'in_bytes': src.ipv4_in_bytes + src.ipv6_in_bytes,
            'out_bytes': src.ipv6_out_bytes + src.ipv6_out_bytes
        }
        self._es.index(index=self._index, id=uuid4().hex, document=peer)

    def __repr__(self):
        return f"ES/{self._index}"
