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

    def graph_flow(self, schedule, src, dst, proto):
        """Create temporary PNG file of RRD flow data
        and returns as byte-stream"""
        src_asn = src.split('-')[0]
        dst_asn = dst.split('-')[0]
        f_path = self._base_path + f"/{src_asn}"
        r_path = self._base_path + f"/{dst_asn}"
        f_rrdfile = f"{f_path}/from__{src}__to__{dst}.rrd"
        r_rrdfile = f"{r_path}/from__{dst}__to__{src}.rrd"
        if os.path.isfile(f_rrdfile) and os.path.isfile(r_rrdfile):
            imgfile = f"/tmp/from__{src}__to__{dst}.png"
            rrdtool.graph(imgfile,
                          "--imgformat", "PNG",
                          "--width", "640",
                          "--height", "320",
                          "--start", f"-1{schedule}",
                          "--title", f"P2P Traffic {src}:{dst}\l",
                          "--vertical-label", "bits / seconds",
                          f"DEF:f_flow={f_rrdfile}:{proto}_bytes:AVERAGE",
                          f"DEF:r_flow={r_rrdfile}:{proto}_bytes:AVERAGE",
                          "CDEF:f_bits=f_flow,8,*",
                          "CDEF:r_bits=r_flow,8,*",
                          "COMMENT:                 \l",
                          "AREA:f_bits#00FF00:Forward",
                          "GPRINT:f_bits:MAX:Max %6.2lf %Sbps",
                          "GPRINT:f_bits:AVERAGE:Avg %6.2lf %Sbps",
                          "GPRINT:f_bits:LAST:Cur %6.2lf %Sbps\l",
                          "LINE:r_bits#FF0000:Reverse",
                          "GPRINT:r_bits:MAX:Max %6.2lf %Sbps",
                          "GPRINT:r_bits:AVERAGE:Avg %6.2lf %Sbps",
                          "GPRINT:r_bits:LAST:Cur %6.2lf %Sbps\l",
            )
            f = open(imgfile, mode="rb")
            data = f.read()
            f.close()
            os.unlink(imgfile)
            return data
        else:
            raise FileNotFoundError([f_rrdfile, r_rrdfile])

    def __repr__(self):
        return "RRD"
