

LOG_MAX = 32

class SFlowStats:

    def __init__(self, logger):
        self._processed_datagrams = 0
        self._processed_samples = 0
        self._not_implemented = 0
        self._parser_errors = 0
        self._unsupported_version = 0
        self._eof_errors = 0
        self._logger = logger

    @property
    def processed_datagrams(self):
        return self._processed_datagrams

    @processed_datagrams.setter
    def processed_datagrams(self, value):
        self._processed_datagrams = value

    @property
    def processed_samples(self):
        return self._processed_samples

    @processed_samples.setter
    def processed_samples(self, value):
        self._processed_samples = value

    @property
    def not_implemented(self):
        return self._not_implemented

    @not_implemented.setter
    def not_implemented(self, value):
        self._not_implemented = value

    @property
    def parser_errors(self):
        return self._parser_errors

    @parser_errors.setter
    def parser_errors(self, value):
        self._parser_errors = value

    @property
    def unsupported_version(self):
        return self._unsupported_version

    @unsupported_version.setter
    def unsupported_version(self, value):
        self._unsupported_version = value

    @property
    def eof_errors(self):
        return self._eof_errors

    @eof_errors.setter
    def eof_errors(self, value):
        self._eof_errors = value

    def log(self):
        self._logger.info(f"[STATS]: {self}")
    def log_info(self, msg):
        self._logger.info(msg)

    def log_debug(self, msg):
        self._logger.debug(msg)

    def log_error(self, msg):
        self._logger.error(msg)

    def cleanup(self):
        self._processed_datagrams = 0
        self._processed_samples = 0
        self._not_implemented = 0
        self._parser_errors = 0
        self._unsupported_version = 0
        self._eof_errors = 0

    def __repr__(self):
        msg = f"DGRAMs: {self.processed_datagrams} | " \
              f"SAMPLEs: {self.processed_samples},  " \
              f"n/impl {self.not_implemented}, " \
              f"pars/err {self.parser_errors}, " \
              f"uns/ver: {self.unsupported_version}, " \
              f"eof: {self.eof_errors} "
        return msg
