



class MACEntry:

    def __init__(self, mac, asnum, name, ipv4, ipv6):
        self._mac = mac
        self._asnum = asnum
        self._name = name
        self._ipv4 = ipv4
        self._ipv6 = ipv6

    @property
    def mac(self):
        return self._mac

    @property
    def asnum(self):
        return self._asnum

    @property
    def name(self):
        return self._name

    @property
    def ipv4(self):
        return self._ipv4

    @property
    def ipv6(self):
        return self._ipv6

    def __eq__(self, other):
        return self.mac == other.mac

    def __hash__(self):
        return hash(self._mac)

    def __repr__(self):
        return f"""
            MAC Entry for {self.name}
            - asn: {self.asnum}
            - mac: {self.mac}
            - ipv4: {self.ipv4}
            - ipv6: {self.ipv6}
        """
