import sys

from nmflows.sflow.exceptions import EthParserException


class EthernetFrameHeader:

    ETHERTYPE_IPV4 = 0x0800
    ETHERTYPE_ARP = 0x0806
    ETHERTYPE_8021Q = 0x8100
    ETHERTYPE_IPV6 = 0x86dd
    ALLOWED_ETHERTYPES = [ETHERTYPE_ARP, ETHERTYPE_8021Q, ETHERTYPE_IPV4, ETHERTYPE_IPV6]

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
    def unpack(cls, data: bytes):
        dst_mac = ''.join('%02x' % b for b in data[0:6])
        src_mac = ''.join('%02x' % b for b in data[6:12])
        type_len = int.from_bytes(data[12:14], byteorder='big', signed=False)
        if type_len in cls.ALLOWED_ETHERTYPES:
            if type_len == cls.ETHERTYPE_8021Q:
                vlan = int.from_bytes(data[14:16], byteorder='big', signed=False) & 0x0fff
                type_len = int.from_bytes(data[16:18], byteorder='big', signed=False)
                return cls(dst_mac, src_mac, vlan, type_len, 18)
            else:
                return cls(dst_mac, src_mac, 0, type_len, 14)
        else:
            raise EthParserException(f"Unrecognized ethertype: {type_len}")


    def __repr__(self):
        return f"""
                                    Src MAC: {self.src_mac}
                                    Dst MAC: {self.dst_mac}
                                    VLAN ID: {self.vlan}
                                    EthType: {self.type}
                                    Length: {self.length}
        """
