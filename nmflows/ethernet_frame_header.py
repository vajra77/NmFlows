import xdrlib

ETHERTYPE_IPV4 = 0x800
ETHERTYPE_ARP = 0x806
ETHTYPE_IPV6 = 0x86DD

ALLOWED_ETHERTYPES = [ hex(ETHERTYPE_ARP), hex(ETHERTYPE_IPV4), hex(ETHTYPE_IPV6)]


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
        eth_type = hex(int.from_bytes(upx.unpack_fopaque(2), 'big'))
        if eth_type in ALLOWED_ETHERTYPES:
            return cls(dst_mac, src_mac, 0, eth_type, 14)
        else:
            # scan back
            position = upx.get_position()
            upx.set_position(position - 2)
            vlan = upx.unpack_uint()
            eth_type = hex(int.from_bytes(upx.unpack_fopaque(2), 'big'))
            assert eth_type in ALLOWED_ETHERTYPES, "unable to recognize ethertype"
            return cls(dst_mac, src_mac, vlan, eth_type, 18)

    def __repr__(self):
        return f"""
                                    Src MAC: {self.src_mac}
                                    Dst MAC: {self.dst_mac}
                                    VLAN ID: {self.vlan}
                                    EthType: {self.type}
                                    Length: {self.length}
        """