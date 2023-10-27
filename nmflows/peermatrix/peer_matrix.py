from nmflows.storage import StorableFlow
from nmflows.utils import get_peer_code
from nmflows.peermatrix.peer_flow import PeerFlow
from datetime import datetime
from elasticsearch import Elasticsearch
from uuid import uuid4


class PeerMatrix:

    def __init__(self):
        self._peers = {}

    def dump(self, es_url):
        es = Elasticsearch(es_url)
        for src_peer in self._peers.values():
            for dst_peer in src_peer.destinations():
                flow = {
                    'src': src_peer.mac,
                    'dst': dst_peer.mac,
                    'ipv4_in_bytes': dst_peer.ipv4_in_bytes,
                    'ipv6_in_bytes': dst_peer.ipv6_in_bytes,
                    'ipv4_out_bytes': dst_peer.ipv4_out_bytes,
                    'ipv6_out_bytes': dst_peer.ipv6_out_bytes,
                    'timestamp': datetime.now()
                }
                es.index(index=src_peer.code, id=uuid4().hex, document=flow)
        # cleanup matrix
        del self._peers


    def add_flow(self, flow: StorableFlow):

        if flow.src_mac in self._peers.keys():
            source = self._peers.get(flow.src_mac)
        else:
            code = get_peer_code(flow.src_mac)
            source = PeerFlow(code, flow.src_mac)

        if source.exists_destination(flow.dst_mac):
            dest = source.get_destination(flow.dst_mac)
        else:
            code = get_peer_code(flow.dst_mac)
            dest = PeerFlow(code, flow.dst_mac)

        if flow.proto == 4:
            dest.account_ipv4_bytes_in(flow.computed_size)
            source.account_ipv4_bytes_out(flow.computed_size)
        else:
            dest.account_ipv6_bytes_in(flow.computed_size)
            source.account_ipv6_bytes_out(flow.computed_size)
