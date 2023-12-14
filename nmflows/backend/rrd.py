from nmflows.peermatrix.peering_flow import PeeringFlow
from .backend import Backend
import rrdtool
import os


class RRDBackend(Backend):

    def __init__(self, base_path):
        self._base_path = base_path

    def store_flows(self, src: PeeringFlow):
        path = self._base_path + f"/AS{src.asnum}"
        if not os.path.exists(path):
            os.makedirs(path)
        for dst in src.destinations:
            filename = f"{path}/from__AS{src.asnum}-{src.mac}__to__AS{dst.asnum}-{dst.mac}.rrd"
            if not os.path.isfile(filename):
                rrdtool.create(filename,
                               "--step", "300",
                               "--start", "now",
                               "DS:ipv4_bytes:ABSOLUTE:600:U:U",
                               "DS:ipv6_bytes:ABSOLUTE:600:U:U",
                               "RRA:AVERAGE:0.5:1:600",
                               "RRA:AVERAGE:0.5:6:700",
                               "RRA:AVERAGE:0.5:24:775",
                               "RRA:AVERAGE:0.5:288:797",
                               "RRA:MAX:0.5:1:600",
                               "RRA:MAX:0.5:6:700",
                               "RRA:MAX:0.5:24:775",
                               "RRA:MAX:0.5:444:797"
                )
            rrdtool.update(filename, "N:%s:%s" % (dst.ipv4_out_bytes * 8, dst.ipv6_out_bytes * 8))

    def store_peer(self, src: PeeringFlow):
        path = self._base_path + f"/AS{src.asnum}"
        if not os.path.exists(path):
            os.makedirs(path)
        filename = f"{path}/iface__AS{src.asnum}-{src.mac}.rrd"
        if not os.path.isfile(filename):
            rrdtool.create(filename,
                           "--step", "300",
                           "--start", "now",
                           "DS:ipv4_in_bytes:ABSOLUTE:600:U:U",
                           "DS:ipv4_out_bytes:ABSOLUTE:600:U:U",
                           "DS:ipv6_in_bytes:ABSOLUTE:600:U:U",
                           "DS:ipv6_out_bytes:ABSOLUTE:600:U:U",
                           "RRA:AVERAGE:0.5:1:600",
                           "RRA:AVERAGE:0.5:6:700",
                           "RRA:AVERAGE:0.5:24:775",
                           "RRA:AVERAGE:0.5:288:797",
                           "RRA:MAX:0.5:1:600",
                           "RRA:MAX:0.5:6:700",
                           "RRA:MAX:0.5:24:775",
                           "RRA:MAX:0.5:444:797"
            )
        rrdtool.update(filename, "N:%s:%s:%s:%s" % (src.ipv4_in_bytes * 8, src.ipv4_out_bytes * 8, src.ipv6_in_bytes * 8, src.ipv6_out_bytes * 8))

    def __repr__(self):
        return "RRD"
