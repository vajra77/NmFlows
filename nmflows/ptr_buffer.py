

class PtrBuffer:

    def __init__(self, data, max_len):
        self._data = data
        self._length = max_len
        self._ptr = 0

    @property
    def data(self):
        return self._data

    @property
    def length(self):
        return self._length

    def read_short(self) -> int:
        ptr = self._ptr
        value = int.from_bytes(self._data[ptr:ptr+2], 'big')
        self._ptr += 2
        return value

    def read_uint(self) -> int:
        ptr = self._ptr
        value = int.from_bytes(self._data[ptr:ptr+4], 'big')
        self._ptr += 4
        return value

    def read_bytes(self, n) -> bytes:
        ptr = self._ptr
        value = self._data[ptr:ptr+n]
        self._ptr += n
        assert self._ptr < self._length
        return value
    