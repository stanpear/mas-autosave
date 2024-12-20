init -990 python:
    store.mas_submod_utils.Submod(
        author="Friends of Monika",
        name="Autosave",
        description=_("Automatic backing up to Github."),
        version="1.0.0"
    )

init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="Autosave",
            user_name="friends-of-monika",
            repository_name="mas-autosave",
            extraction_depth=2
        )

init -980 python hide:
    import store
    import os

    script_dir = store.fom_getScriptDir(fallback="game/Submods/Autosave")
    script_dir = renpy.config.basedir + "/" + script_dir
    os.environ["SSL_CERT_FILE"] = script_dir + "/misc/cacert.pem"
