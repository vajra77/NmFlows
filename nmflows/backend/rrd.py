from nmflows.peermatrix.peering_flow import PeeringFlow
from .backend import Backend
import os


class RRDBackend(Backend):

    def __init__(self, base_path):
        self._base_path = base_path

    def store_flows(self, src: PeeringFlow):
        path = self._base_path + f"/{src.name}"
        if not os.path.exists(path):
            os.makedirs(path)
        for dst in src.destinations:
            filename = f"{path}/from_{src.name}-{src.mac}_to_{dst.name}-{dst.mac}.rrd"

    def store_peer(self, src: PeeringFlow):
        pass
