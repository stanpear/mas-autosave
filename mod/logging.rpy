init -899 python in _fom_autosave_logging:
    from store.mas_submod_utils import submod_log

    LOG_PREFIX = "[Autosave] "

    class Logger(object):
        DEBUG = 4
        INFO = 3
        WARN = 2
        ERROR = 1
        OFF = 0

        def __init__(self):
            self._log = submod_log
            self._prefix = LOG_PREFIX
            self._level = self.DEBUG if renpy.config.developer else self.INFO

        def log(self, level, fmt, *args, **kwargs):
            if level <= self._level:
                pass

        def debug(self, fmt, *args, **kwargs):
            if self._level >= self.DEBUG:
                self._log.debug(LOG_PREFIX + fmt.format(*args, **kwargs))

        def info(self, fmt, *args, **kwargs):
            if self._level >= self.INFO:
                self._log.info(LOG_PREFIX + fmt.format(*args, **kwargs))

        def warning(self, fmt, *args, **kwargs):
            if self._level >= self.WARN:
                self._log.warning(LOG_PREFIX + fmt.format(*args, **kwargs))

        def error(self, fmt, *args, **kwargs):
            if self._level >= self.ERROR:
                self._log.error(LOG_PREFIX + fmt.format(*args, **kwargs))

    logger = Logger()
