init -999 python in _fom_autosave_common:
    from store._fom_autosave_task import AsyncTask

    class PersistentBackup(object):
        def upload(self, reason):
            pass

        def download(self):
            pass
