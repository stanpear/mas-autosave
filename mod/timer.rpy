default persistent._fom_autosave_last_autosave = None

init -1000 python in _fom_autosave_timer:
    from datetime import datetime, timedelta
    from store import persistent

    BACKUP_FREQ = {
        0: ("Off", None),
        1: ("Hourly", timedelta(seconds=3600)),
        2: ("Daily", timedelta(days=1)),
        3: ("Weekly", timedelta(days=7)),
        4: ("Monthly", timedelta(days=30))
    }

init 10 python in _fom_autosave_timer:
    from store.mas_submod_utils import functionplugin
    from store._fom_autosave_logging import logger

    def has_period_elapsed():
        last = persistent._fom_autosave_last_autosave
        freq = persistent._fom_autosave_config_common["backup_freq"]
        now = datetime.now()

        _, delta = BACKUP_FREQ[freq]
        if delta is None:
            return False
        if last is None:
            return True

        return now - last > delta

    def try_do_backup():
        def on_backup_complete():
            persistent._fom_autosave_last_autosave = datetime.now()

        if has_period_elapsed():
            logger.debug("Attempting timed backup (may be overridden if remote is not configured.)")
            freq = persistent._fom_autosave_config_common["backup_freq"]
            name, _ = BACKUP_FREQ[freq]
            store._fom_autosave_common.backup_persistent(
                reason="{0} auto-backup".format(name),
                on_complete=on_backup_complete)

    @functionplugin("ch30_hour")
    def do_hourly():
        try_do_backup()

    @functionplugin("ch30_start")
    def do_start():
        try_do_backup()
