from nmflows.utils.buffer import Buffer


class EthernetHeader:

    ETHERTYPE_IPV4 = 0x0800
    ETHERTYPE_ARP = 0x0806
    ETHERTYPE_8021Q = 0x8100
    ETHERTYPE_IPV6 = 0x86dd

    ALLOWED_ETHERTYPES = [ETHERTYPE_ARP, ETHERTYPE_8021Q, ETHERTYPE_IPV4, ETHERTYPE_IPV6]

    def __init__(self, dst_mac, src_mac, vlan_id, eth_type, length):
        self._destination_mac = dst_mac
        self._source_mac = src_mac
        self._vlan = vlan_id
        self._ether_type = eth_type
        self._length = length

    @property
    def destination_mac(self):
        return self._destination_mac

    @property
    def source_mac(self):
        return self._source_mac

    @property
    def vlan(self):
        return self._vlan

    @property
    def ether_type(self):
        return self._ether_type

    @property
    def length(self):
        return self._length

    @classmethod
    def from_bytes(cls, data):
        buffer = Buffer.from_bytes(data)
        dst_mac = ''.join('%02x' % b for b in buffer.read_bytes(0,6))
        src_mac = ''.join('%02x' % b for b in buffer.read_bytes(6,6))
        type_len = buffer.read_short(12) #int.from_bytes(data[12:14], byteorder='big', signed=False)
        if type_len in cls.ALLOWED_ETHERTYPES:
            if type_len == cls.ETHERTYPE_8021Q:
                vlan = buffer.read_short(14) & 0x0fff #int.from_bytes(data[14:16], byteorder='big', signed=False) & 0x0fff
                type_len = buffer.read_short(16) # from_bytes(data[16:18], byteorder='big', signed=False)
                return cls(dst_mac, src_mac, vlan, type_len, 18)
            else:
                return cls(dst_mac, src_mac, 0, type_len, 14)
        else:
            raise NotImplementedError('unknown_ethtype_in_datalink_header')
