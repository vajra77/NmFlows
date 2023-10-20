import xdrlib


class EthernetFrameHeader:

    def __init__(self, dst_mac, src_mac, e_type, length):
        self._dst_mac = dst_mac
        self._src_mac = src_mac
        self._type = e_type
        self._length = length

    @property
    def src_mac(self):
        return self._src_mac

    @property
    def dst_mac(self):
        return self._dst_mac

    @property
    def type(self):
        return self._type

    @property
    def length(self):
        return self._length

    @classmethod
    def unpack(cls, upx: xdrlib.Unpacker):
        # dst_mac = ':'.join('%02x' % b for b in upx.unpack_fopaque(6))
        # src_mac = ':'.join('%02x' % b for b in upx.unpack_fopaque(6))
        # length = int.from_bytes(upx.unpack_fopaque(2), "big")
        # upx.unpack_fopaque(hdr_length - 14)
        dst_mac = ''.join('%02x' % b for b in upx.unpack_fopaque(6))
        src_mac = ''.join('%02x' % b for b in upx.unpack_fopaque(6))
        eth_type = hex(int.from_bytes(upx.unpack_fopaque(2), 'little'))
        return cls(dst_mac, src_mac, eth_type, 14)

    def __repr__(self):
        return f"""
                                    Src MAC: {self.src_mac}
                                    Dst MAC: {self.dst_mac}
                                    EthType: {self.type}
                                    Length: {self.length}
        """