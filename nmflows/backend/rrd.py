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
            rrdtool.update(filename, "N:%s:%s" % (dst.ipv4_out_bytes, dst.ipv6_out_bytes))

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
        rrdtool.update(filename, "N:%s:%s:%s:%s" % (src.ipv4_in_bytes, src.ipv4_out_bytes, src.ipv6_in_bytes, src.ipv6_out_bytes))

    def graph_flow(self, schedule, src, dst):
        """Create temporary PNG file of RRD flow data
        and returns as byte-stream"""
        src_asn = src.split('-')[0]
        path = self._base_path + f"/{src_asn}"
        rrdfile = f"{path}/from__{src}__to__{dst}.rrd"
        if os.path.isfile(rrdfile):
            imgfile = f"/tmp/from__{src}__to__{dst}.png"
            rrdtool.graph(imgfile,
                          "--imgformat", "PNG",
                          "--width", "640",
                          "--height", "320",
                          "--start", f"-1{schedule}",
                          "--title", f"Traffic flowing from {src} to {dst}",
                          "--vertical-label", "bits / seconds"
                          f"DEF:flow4={rrdfile}:ipv4_bytes:AVERAGE",
                          f"DEF:flow6={rrdfile}:ipv6_bytes:AVERAGE",
                          "CDEF:bits4=flow4,8,*",
                          "CDEF:bits6=flow6,8,*",
                          "COMMENT:                 \l",
                          "AREA:bits4#00FF00:IPv4",
                          "GPRINT:bits4:MAX:Max %6.2lf %Sbps",
                          "GPRINT:bits4:AVERAGE:Avg %6.2lf %Sbps",
                          "GPRINT:bits4:LAST:Cur %6.2lf %Sbps\l",
                          "LINE:bits6#FF0000:IPv6",
                          "GPRINT:bits6:MAX:Max %6.2lf %Sbps",
                          "GPRINT:bits6:AVERAGE:Avg %6.2lf %Sbps",
                          "GPRINT:bits6:LAST:Cur %6.2lf %Sbps\l",
            )
            f = open(imgfile, mode="rb")
            data = f.read()
            f.close()
            os.unlink(imgfile)
            return data
        else:
            raise FileNotFoundError(rrdfile)

    def __repr__(self):
        return "RRD"
