init -1999 python in _fom_autosave_persistent:
    import renpy

    def get_persistent_path():
        loadsave_loc = renpy.loadsave.location
        if hasattr(loadsave_loc, "locations"):
            return loadsave_loc.active_locations()[0].persistent
        return loadsave_loc.persistent
