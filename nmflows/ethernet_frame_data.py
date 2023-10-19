import xdrlib


class EthernetFrameData:

    def __init__(self, length, src_mac, dst_mac, eth):
        self._length = length
        self._source_mac = src_mac
        self._destination_mac = dst_mac
        self._ethertype = eth


    @property
    def length(self):
        return self._length

    @property
    def source_mac(self):
        return self._source_mac

    @property
    def destination_mac(self):
        return self._destination_mac

    @property
    def ethertype(self):
        return self._ethertype

    @classmethod
    def unpack(cls, upx: xdrlib.Unpacker):
        length = upx.unpack_uint()
        src_mac = upx.unpack_uint()
        dst_mac = upx.unpack_uint()
        eth_type = upx.unpack_uint()
        return cls(length, src_mac, dst_mac, eth_type)

    def __repr__(self):
        return f"""
                            Class: {self.__class__.__name__}
                            Length: {self.length}
                            Source MAC: {self.source_mac}
                            Destin MAC: {self.destination_mac}
                            EtherType: {self.ethertype}
        """
