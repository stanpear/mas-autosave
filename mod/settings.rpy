default persistent._fom_autosave_config = None

init -1000 python:
    if persistent._fom_autosave_config is None:
        persistent._fom_autosave_config = {}

screen fom_autosave_settings():
    pass
