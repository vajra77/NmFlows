import xdrlib
import socket


class EthernetFrameHeader:

    def __init__(self, dst_mac, src_mac, vlan, length):
        self._dst_mac = dst_mac
        self._src_mac = src_mac
        self._vlan = vlan
        self._length = length

    @property
    def src_mac(self):
        return self._src_mac

    @property
    def dst_mac(self):
        return self._dst_mac

    @property
    def vlan(self):
        return self._vlan

    @property
    def length(self):
        return self._length

    @classmethod
    def unpack(cls, upx: xdrlib.Unpacker, hdr_length):
        # length = upx.unpack_uint()
        # dst_mac = ':'.join('%02x' % b for b in upx.unpack_fopaque(6))
        # src_mac = ':'.join('%02x' % b for b in upx.unpack_fopaque(6))
        # # vlan = upx.unpack_uint()
        # vlan = 0
        # payload_length = int.from_bytes(upx.unpack_fopaque(2), "big")
        # upx.unpack_fopaque(hdr_length - 18)
        length = upx.unpack_uint()
        dst_mac = upx.unpack_uint()
        src_mac = upx.unpack_uint()
        ethertype = upx.unpack_uint()
        upx.unpack_fopaque(hdr_length - 32)
        return cls(dst_mac, src_mac, 0, length)

    def __repr__(self):
        return f"""
                                    Dst MAC: {self.dst_mac}
                                    Src MAC: {self.src_mac}
                                    VLAN: {self.vlan & 0b111111111111}
                                    Length: {self.length}
        """