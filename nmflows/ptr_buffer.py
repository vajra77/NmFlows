

UNSIGNED_SHORT_SIZE = 2
UNSIGNED_INT_SIZE = 4

class NenBuffer(Exception):

    def __init__(self, msg):
        super().__init__(f"#buf not enough bytes to read: {msg}")


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

    @property
    def eof(self):
        return self._ptr == self._length - 1

    def reset(self):
        self._ptr = 0

    def available_data(self):
        return self._length - self._ptr

    def read_short(self) -> int:
        if self.available_data() >= UNSIGNED_SHORT_SIZE:
            ptr = self._ptr
            value = int.from_bytes(self._data[ptr:ptr + UNSIGNED_SHORT_SIZE], 'big')
            self._ptr += UNSIGNED_SHORT_SIZE
            return value
        else:
            raise NenBuffer(f"2 requested, {self.available_data()} available")

    def read_uint(self) -> int:
        if self.available_data() >= UNSIGNED_INT_SIZE:
            ptr = self._ptr
            value = int.from_bytes(self._data[ptr:ptr+UNSIGNED_INT_SIZE], 'big')
            self._ptr += UNSIGNED_INT_SIZE
            return value
        else:
            raise NenBuffer(f"4 requested, {self.available_data()} available")

    def read_bytes(self, n) -> bytes:
        if self.available_data() >= n:
            ptr = self._ptr
            value = self._data[ptr:ptr+n]
            self._ptr += n
            return value
        else:
            raise NenBuffer(f"{n} requested, {self.available_data()} available")

    def skip(self, n):
        ptr = self._ptr + n
        if ptr >= self._length:
            ptr = self._length - 1
        self._ptr = ptr
