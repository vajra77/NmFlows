

class Record:

    FORMAT_RAW_PACKET = 1
    FORMAT_ETHERNET_DATA_FRAME = 2
    FORMAT_IPV4_DATA = 3
    FORMAT_IPV6_DATA = 4
    FORMAT_EXT_SWITCH_DATA = 1001
    FORMAT_EXT_ROUTER_DATA = 1002

    def __init__(self, sformat, length):
        self._format = sformat
        self._length = length

    @property
    def format(self):
        return self._format

    def length(self):
        return self._length