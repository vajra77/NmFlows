from nmflows.peermatrix.peering_flow import PeeringFlow
from .backend import Backend
from datetime import datetime
import rrdtool
import os
import pwd
import grp


def _chown(filename):
    uid = pwd.getpwnam("root").pw_uid
    gid = grp.getgrnam("www-data").gr_gid
    os.chown(filename, uid, gid)

class RRDBackend(Backend):

    def __init__(self, base_path, base_gamma=1):
        self._base_path = base_path
        self._base_gamma = base_gamma

    @property
    def base_path(self):
        return self._base_path

    @property
    def base_gamma(self):
        return self._base_gamma

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
                               "DS:ipv4_bytes:COUNTER:600:U:U",
                               "DS:ipv6_bytes:COUNTER:600:U:U",
                               "RRA:AVERAGE:0.5:1:600",
                               "RRA:AVERAGE:0.5:6:700",
                               "RRA:AVERAGE:0.5:24:775",
                               "RRA:AVERAGE:0.5:288:797",
                               "RRA:MAX:0.5:1:600",
                               "RRA:MAX:0.5:6:700",
                               "RRA:MAX:0.5:24:775",
                               "RRA:MAX:0.5:444:797")
                _chown(filename)
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
                           "DS:ipv4_in_bytes:COUNTER:600:U:U",
                           "DS:ipv4_out_bytes:COUNTER:600:U:U",
                           "DS:ipv6_in_bytes:COUNTER:600:U:U",
                           "DS:ipv6_out_bytes:COUNTER:600:U:U",
                           "RRA:AVERAGE:0.5:1:600",
                           "RRA:AVERAGE:0.5:6:700",
                           "RRA:AVERAGE:0.5:24:775",
                           "RRA:AVERAGE:0.5:288:797",
                           "RRA:MAX:0.5:1:600",
                           "RRA:MAX:0.5:6:700",
                           "RRA:MAX:0.5:24:775",
                           "RRA:MAX:0.5:444:797")
            _chown(filename)
        rrdtool.update(filename, "N:%s:%s:%s:%s" % (src.ipv4_in_bytes, src.ipv4_out_bytes,
                                                    src.ipv6_in_bytes, src.ipv6_out_bytes))

    def graph_flow(self, schedule, src, dst, proto):
        """Create temporary PNG file of RRD flow data
        and returns as byte-stream"""
        src_asn, src_mac = src.split('-')
        dst_asn, dst_mac = dst.split('-')
        f_path = self._base_path + f"/{src_asn}"
        r_path = self._base_path + f"/{dst_asn}"
        f_rrdfile = f"{f_path}/from__{src}__to__{dst}.rrd"
        r_rrdfile = f"{r_path}/from__{dst}__to__{src}.rrd"
        if os.path.isfile(f_rrdfile) and os.path.isfile(r_rrdfile):
            gamma = 8 * self._base_gamma
            imgfile = f"/tmp/from__{src}__to__{dst}.png"
            date = datetime.today()
            rrdtool.graph(imgfile,
                          "--imgformat", "PNG",
                          "--width", "640",
                          "--height", "256",
                          "--start", f"-1{schedule}",
                          "--title", f"{proto.upper()} Traffic {src_asn}[:{src_mac[-2:]}] -> {dst_asn}[:{dst_mac[-2:]}]\r\r",
                          "--watermark", f"Generated: {date} / NmFlows by Namex IXP",
                          "--vertical-label", "bits / seconds",
                          f"DEF:f_flow={f_rrdfile}:{proto}_bytes:AVERAGE",
                          f"DEF:r_flow={r_rrdfile}:{proto}_bytes:AVERAGE",
                          f"CDEF:f_bits=f_flow,{gamma},*",
                          f"CDEF:r_bits=r_flow,{gamma},*",
                          "COMMENT:                 \l",
                          f"AREA:r_bits#00FF00:{src_asn} <- {dst_asn}\t",
                          "GPRINT:r_bits:MAX:Max %3.2lf%s\t",
                          "GPRINT:r_bits:AVERAGE:Avg %3.2lf%s\t",
                          "GPRINT:r_bits:LAST:Cur %3.2lf%s\l",
                          f"LINE:f_bits#0000FF:{src_asn} -> {dst_asn}\t",
                          "GPRINT:f_bits:MAX:Max %3.2lf%s\t",
                          "GPRINT:f_bits:AVERAGE:Avg %3.2lf%s\t",
                          "GPRINT:f_bits:LAST:Cur %3.2lf%s\l",
                          "COMMENT:                 \l",
            )
            f = open(imgfile, mode="rb")
            data = f.read()
            f.close()
            os.unlink(imgfile)
            return data
        else:
            f = open('static/404.png', mode='rb')
            data = f.read()
            f.close()
            return data

    def graph_peer(self, schedule, src, proto):
        src_asn, src_mac = src.split('-')
        if_path = self._base_path + f"/{src_asn}"
        rrdfile = f"{if_path}/iface__{src}.rrd"
        if os.path.isfile(rrdfile):
            gamma = 8 * self._base_gamma
            imgfile = f"/tmp/iface__{src}.png"
            date = datetime.today()
            rrdtool.graph(imgfile,
                          "--imgformat", "PNG",
                          "--width", "640",
                          "--height", "256",
                          "--start", f"-1{schedule}",
                          "--title", f"{proto.upper()} Interface Traffic {src_asn}[:{src_mac[-2:]}]\r\r",
                          "--watermark", f"Generated: {date} / NmFlows by Namex IXP",
                          "--vertical-label", "bits / seconds",
                          f"DEF:in_flow={rrdfile}:{proto}_in_bytes:AVERAGE",
                          f"DEF:out_flow={rrdfile}:{proto}_out_bytes:AVERAGE",
                          f"CDEF:in_bits=in_flow,{gamma},*",
                          f"CDEF:out_bits=out_flow,{gamma},*",
                          "COMMENT:                 \l",
                          f"AREA:out_bits#00FF00:Outbound \t",
                          "GPRINT:out_bits:MAX:Max %3.2lf%s\t",
                          "GPRINT:out_bits:AVERAGE:Avg %3.2lf%s\t",
                          "GPRINT:out_bits:LAST:Cur %3.2lf%s\l",
                          f"LINE:in_bits#0000FF:Inbound\t",
                          "GPRINT:in_bits:MAX:Max %3.2lf%s\t",
                          "GPRINT:in_bits:AVERAGE:Avg %3.2lf%s\t",
                          "GPRINT:in_bits:LAST:Cur %3.2lf%s\l",
                          "COMMENT:                 \l",
            )
            f = open(imgfile, mode="rb")
            data = f.read()
            f.close()
            os.unlink(imgfile)
            return data
        else:
            f = open('static/404.png', mode='rb')
            data = f.read()
            f.close()
            return data

    def __repr__(self):
        return "RRD"
