init -999 python in _fom_autosave_common:
    from store._fom_autosave_task import AsyncTask

    class PersistentBackup(object):
        def upload(self, reason):
            pass

        def download(self):
            pass

    def backup_persistent(reason="autosave"):
        renpy.show_screen("fom_autosave_common__save", reason)


screen fom_autosave_common__save(reason, on_complete=None, on_error=None):
    default promise = store._fom_autosave_task.AsyncTask(store._fom_autosave_github.backup_service.upload, reason)
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
            text "Backing up persistent..." at fom_autosave_common__save__blink()

        elif error is not None:
            text "Backing up failed, see logs." at fom_autosave_common__save__fade()
            timer 1.0 action [Hide("fom_autosave_common__save"),
                              Function(on_error, error) if on_error is not None else NullAction()]

        else:
            text "Backed up successfully." at fom_autosave_common__save__fade()
            timer 1.0 action [Hide("fom_autosave_common__save"),
                              Function(on_complete) if on_complete is not None else NullAction()]

transform fom_autosave_common__save__blink(min_opacity=0.2, max_opacity=0.7, duration=1.0):
    alpha max_opacity
    linear duration alpha min_opacity
    linear duration alpha max_opacity
    repeat

transform fom_autosave_common__save__fade(alpha=1.0, duration=1.0):
    linear duration alpha 0.0
