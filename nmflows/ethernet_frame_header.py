import xdrlib
import socket


class EthernetFrameHeader:

    def __init__(self, dst_mac, src_mac, length):
        self._dst_mac = dst_mac
        self._src_mac = src_mac
        self._length = length

    @property
    def src_mac(self):
        return self._src_mac

    @property
    def dst_mac(self):
        return self._dst_mac

    @property
    def length(self):
        return self._length

    @classmethod
    def unpack(cls, upx: xdrlib.Unpacker, hdr_length):
        # dst_mac = ':'.join('%02x' % b for b in upx.unpack_fopaque(6))
        # src_mac = ':'.join('%02x' % b for b in upx.unpack_fopaque(6))
        # length = int.from_bytes(upx.unpack_fopaque(2), "big")
        # upx.unpack_fopaque(hdr_length - 14)
        src_mac = ':'.join('%02x' % b for b in upx.unpack_fopaque(6))
        dst_mac = ':'.join('%02x' % b for b in upx.unpack_fopaque(6))
        length = int.from_bytes(upx.unpack_fopaque(2), 'little')
        upx.unpack_fopaque(hdr_length - 14)
        return cls(dst_mac, src_mac, length)

    def __repr__(self):
        return f"""
                                    Dst MAC: {self.dst_mac}
                                    Src MAC: {self.src_mac}
                                    Length: {self.length}
        """