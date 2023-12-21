import socket


class Buffer:

    def __init__(self, data):
        self._data = data

    @property
    def length(self):
        return len(self._data)

    def read_uint(self, start):
        value = int.from_bytes(self._data[start:start+4], byteorder='big', signed=False)
        return value & 0xffffffff

    def read_short(self, start):
        value = int.from_bytes(self._data[start:start+2], byteorder='big', signed=False)
        return value & 0xffff

    def read_byte(self, start):
        value = int.from_bytes(self._data[start:start+1], byteorder='big', signed=False)
        return value & 0xff

    def read_bytes(self, start, blen):
        return self._data[start:start+blen]

    def read_ipv4_address(self, start):
        return socket.inet_ntop(socket.AF_INET, self._data[start:start+4])

    def read_ipv6_address(self, start):
        return socket.inet_ntop(socket.AF_INET6, self._data[start:start+16])

    @classmethod
    def from_bytes(cls, data):
        return cls(data)
