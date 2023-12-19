

class SFlowStats:

    def __init__(self):
        self._processed_datagrams = 0
        self._not_implemented = 0
        self._parser_errors = 0
        self._unsupported_version = 0
        self._eof_errors = 0

    @property
    def processed_datagrams(self):
        return self._processed_datagrams

    @property
    def not_implemented(self):
        return self._not_implemented

    @property
    def parser_errors(self):
        return self._parser_errors

    @property
    def unsupported_version(self):
        return self._unsupported_version

    @property
    def eof_errors(self):
        return self._eof_errors

    def inc_processed_datagrams(self):
        self._processed_datagrams += 1

    def inc_not_implemented(self):
        self._not_implemented += 1

    def inc_parser_errors(self):
        self._parser_errors += 1

    def inc_unsupported_version(self):
        self._unsupported_version += 1

    def inc_eof_errors(self):
        self._eof_errors += 1

    def __repr__(self):
        msg = f"Processed: {self.processed_datagrams} | N/Impl {self.not_implemented} | Pars/err {self.parser_errors} " \
              f"| Uns/ver: {self.unsupported_version} | EOF {self.eof_errors} "
        return msg
