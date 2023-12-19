import logging
from datetime import datetime


def _tstamp(msg):
    now = datetime.now()
    return f"{now}: {msg}"

class StatLogger:

    def __init__(self, logfile, debug):
        self._logger = logging.getLogger(__name__)

        if debug:
            self._logger.setLevel(logging.DEBUG)
        else:
            self._logger.setLevel(logging.INFO)

        self._logger.propagate = False
        self._fh = logging.FileHandler(logfile, "w")

        if debug:
            self._fh.setLevel(logging.DEBUG)
        else:
            self._fh.setLevel(logging.INFO)

        self._logger.addHandler(self._fh)
        self._counters = {}

    @property
    def keep_fds(self):
        return [self._fh.stream.fileno()]

    def debug(self, msg):
        self._logger.debug(_tstamp(msg))

    def info(self, msg):
        self._logger.info(_tstamp(msg))

    def error(self, msg):
        self._logger.info(_tstamp(msg))

    def increment_counter(self, key):
        if key in self._counters.keys():
            self._counters[key] += 1
        else:
            self._counters[key] = 1

    def log_counters(self):
        self._logger.info(self)

    def reset_counters(self):
        for k in self._counters.keys():
            self._counters[k] = 0

    def __repr__(self):
        res = "COUNTERS: "
        for c, value in self._counters.items():
            res += f"{c}: {value}, "
        return _tstamp(res)
