init -999 python in _fom_autosave_common:
    from store._fom_autosave_task import AsyncTask

    class PersistentBackup(object):
        def is_configured(self):
            pass

        def upload(self):
            pass

        def download(self):
            pass

init 100 python in _fom_autosave_common:
    from store._fom_autosave_github import GithubBackup
    from store import persistent
    import store

    from datetime import datetime

    SELECTED_BACKUP = GithubBackup # only Github for now
    is_any_pending = False

    def is_safe_to_backup():
        return not store.mas_globals.tt_detected

    def backup_persistent(reason="autosave", on_complete=None, on_error=None):
        def local_on_complete():
            global is_any_pending
            is_any_pending = False

            persistent._fom_autosave_last_save = datetime.now()
            if on_complete is not None:
                on_complete()

        backup_service = SELECTED_BACKUP(reason)
        if backup_service.is_configured() and is_safe_to_backup():
            global is_any_pending
            is_any_pending = True

            renpy.show_screen("fom_autosave_common__save", backup_service,
                local_on_complete, on_error)

screen fom_autosave_common__save(backup_service, on_complete=None, on_error=None):
    default promise = store._fom_autosave_task.AsyncTask(backup_service.upload)
    timer 0.5 action Function(renpy.restart_interaction) repeat True
    on "show" action Function(promise.run_in_background)

    python:
        try:
            if promise.is_complete():
                promise.get()
            error = None
        except Exception as e:
            store._fom_autosave_logging.logger.error("Failed to upload save: {0}", e)
            error = e

    fixed:
        xpos 10
        ypos 10

        if not promise.is_complete():
            text "Backing up persistent..." at fom_autosave_common__blink()

        elif error is not None:
            text "Backing up failed, see logs." at fom_autosave_common__fade()
            timer 1.0 action [Hide("fom_autosave_common__save"),
                              Function(on_error, error) if on_error is not None else NullAction()]

        else:
            text "Backed up successfully." at fom_autosave_common__fade()
            timer 1.0 action [Hide("fom_autosave_common__save"),
                              Function(on_complete) if on_complete is not None else NullAction()]

transform fom_autosave_common__blink(min_opacity=0.2, max_opacity=0.7, duration=1.0):
    alpha max_opacity
    linear duration alpha min_opacity
    linear duration alpha max_opacity
    repeat

transform fom_autosave_common__fade(alpha=1.0, duration=1.0):
    linear duration alpha 0.0
