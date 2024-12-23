default persistent._fom_autosave_config = None

init -1000 python:
    if persistent._fom_autosave_config is None:
        persistent._fom_autosave_config = {}

init -1000 python in _fom_autosave_config:
    from store import persistent

    def get_remotes():
        if "remote" not in persistent._fom_autosave_config:
            persistent._fom_autosave_config["remote"] = {}
        return persistent._fom_autosave_config["remote"]

    def has_remote_config(key):
        return key in get_remotes()

    def get_remote_config(key):
        remotes = get_remotes()
        return remotes.get(key)

    def set_remote_config(key, config):
        remotes = get_remotes()
        remotes[key] = config


screen fom_autosave_settings():
    use fom_autosave_settings_github_options()
