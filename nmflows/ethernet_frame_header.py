import xdrlib

ETHERTYPE_IPV4 = 0x800
ETHERTYPE_ARP = 0x806
ETHERTYPE_8021Q = 0x8100
ETHERTYPE_IPV6 = 0x86DD


ALLOWED_ETHERTYPES = [ETHERTYPE_ARP, ETHERTYPE_8021Q, ETHERTYPE_IPV4, ETHERTYPE_IPV6]


class EthernetFrameHeader:

    def __init__(self, dst_mac, src_mac, vlan, e_type, length):
        self._dst_mac = dst_mac
        self._src_mac = src_mac
        self._vlan = vlan
        self._type = e_type
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
    def type(self):
        return self._type

    @property
    def length(self):
        return self._length

    @classmethod
    def unpack(cls, upx: xdrlib.Unpacker):
        dst_mac = ''.join('%02x' % b for b in upx.unpack_fopaque(6))
        src_mac = ''.join('%02x' % b for b in upx.unpack_fopaque(6))
        eth_type = int.from_bytes(upx.unpack_fopaque(2), 'big')

        if eth_type < 1536:
            return cls(dst_mac, src_mac, 0, eth_type, 14)
        elif eth_type in ALLOWED_ETHERTYPES:
            if eth_type == ETHERTYPE_8021Q:
                vlan = int.from_bytes(upx.unpack_fopaque(2), 'big')
                eth_type = int.from_bytes(upx.unpack_fopaque(2), 'big')
                return cls(dst_mac, src_mac, vlan, eth_type, 18)
            else:
                return cls(dst_mac, src_mac, 0, eth_type, 14)
        else:
            raise Exception(f"Unrecognized ethertype: {eth_type}")

    def __repr__(self):
        return f"""
                                    Src MAC: {self.src_mac}
                                    Dst MAC: {self.dst_mac}
                                    VLAN ID: {self.vlan}
                                    EthType: {self.type}
                                    Length: {self.length}
        """