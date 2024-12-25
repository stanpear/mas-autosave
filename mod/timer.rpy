default persistent._fom_autosave_last_autosave = None

init -1000 python in _fom_autosave_timer:
    from store import persistent
    from datetime import datetime, timedelta

    BACKUP_FREQ = {
        0: ("Off", None),
        1: ("Hourly", timedelta(seconds=3600)),
        2: ("Daily", timedelta(days=1)),
        3: ("Weekly", timedelta(days=7)),
        4: ("Monthly", timedelta(days=30))
    }

init 10 python in _fom_autosave_timer:
    from store.mas_submod_utils import functionplugin

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

    @functionplugin("ch30_hour")
    def do_hourly():
        def on_backup_complete():
            persistent._fom_autosave_last_autosave = datetime.now()

        if has_period_elapsed():
            freq = persistent._fom_autosave_config_common["backup_freq"]
            name, _ = BACKUP_FREQ[freq]
            renpy.show_screen(
                "fom_autosave_common__save",
                "{0} auto-backup".format(name),
                on_backup_complete
            )
