default persistent._fom_autosave_config_common = None
default persistent._fom_autosave_config_github = None

init -1000 python:
    if persistent._fom_autosave_config_common is None:
        persistent._fom_autosave_config_common = {
            "backup_freq": 0
        }

    if persistent._fom_autosave_config_github is None:
        persistent._fom_autosave_config_github = {
            "repo_name": "",
            "commit_fmt": "[[Autosave] Persistent backup ([reason])"
        }

init -978 python in _fom_autosave_config:
    from store import mas_registerAPIKey
    from store import persistent

    def on_github_key_change(api_key):
        persistent._fom_autosave_config_github["repo_name"] = ""
        return True, ""

    KEY_ID_GITHUB = "fom_autosave_config_github_apikey"
    mas_registerAPIKey(KEY_ID_GITHUB, _("[[Autosave] Github API token"), on_change=on_github_key_change)

    BACKUP_FREQ_NAMES = {
        0: "Off",
        1: "Hourly",
        2: "Daily",
        3: "Weekly",
        4: "Monthly"
    }


screen fom_autosave_settings():
    $ github_api_key = mas_getAPIKey(store._fom_autosave_config.KEY_ID_GITHUB)
    $ repo_name = persistent._fom_autosave_config_github.get("repo_name", None)
    $ tooltip_disp = renpy.get_screen("submods", "screens").scope["tooltip"]

    vbox:
        style_prefix "check"
        xmaximum 800
        xfill True

        text _("Github setup checklist:")
        hbox:
            if github_api_key:
                text _("- API token {color=#84cc16}is set{/color}")
            else:
                text _("- API token {color=#ef4444}is not set{/color}")

            textbutton _("Open API keys menu"):
                action Show("mas_apikeys")
                hovered SetField(tooltip_disp, "value", _("Click to open API keys menu."))
                unhovered SetField(tooltip_disp, "value", tooltip_disp.default)
                xoffset -12

        hbox:
            if repo_name:
                text _("- Repository {color=#84cc16}is set{/color}{space=10}([repo_name])")
            else:
                text _("- Repository {color=#ef4444}is not selected{/color}")

            textbutton _("Select repository"):
                sensitive bool(github_api_key)
                action Show("fom_autosave_settings__repo_select")
                hovered SetField(tooltip_disp, "value", _("Click to select repository to use for backing up."))
                unhovered SetField(tooltip_disp, "value", tooltip_disp.default)
                xoffset -12

        vbox:
            use fom_autosave_settings__slider(
                title=_("Backup frequency"),
                value=DictValue(persistent._fom_autosave_config_common, "backup_freq", offset=0, range=len(store._fom_autosave_config.BACKUP_FREQ_NAMES) - 1),
                display=store._fom_autosave_config.BACKUP_FREQ_NAMES[persistent._fom_autosave_config_common["backup_freq"]],
                tooltip=_("You can set automatic backup frequency by adjusting this slider."))

        textbutton _("Force save"):
            sensitive github_api_key and repo_name
            action Show("fom_autosave_settings__force_save")
            hovered SetField(tooltip_disp, "value", _("Click to force save the persistent to Github."))
            unhovered SetField(tooltip_disp, "value", tooltip_disp.default)

screen fom_autosave_settings__repo_select():
    default github_api_key = mas_getAPIKey(store._fom_autosave_config.KEY_ID_GITHUB)
    default promise = store._fom_autosave_task.AsyncTask(store._fom_autosave_github.get_own_repos, github_api_key)

    timer 0.5 action Function(renpy.restart_interaction) repeat True
    on "show" action Function(promise.run_in_background)

    default repos = None
    default error = None

    python:
        try:
            if promise.is_complete():
                status, repos = promise.get()
        except Exception as e:
            if error is not None:
                store._fom_autosave_logging.logger.error("Failed to load repositories: {0}", e)
                error = e

    use fom_autosave_screens__confirm(xmaximum=500, ymaximum=400, spacing=30):
        style_prefix "confirm"

        text _("Select repository"):
            style "confirm_prompt"
            xalign 0.5

        if not promise.is_complete():
            text _("Loading..."):
                xalign 0.5
                text_align 0.5
        elif error is not None:
            text _("Failed to load repositories. Check logs."):
                xalign 0.5
                text_align 0.5
        else:
            hbox:
                viewport id "repos":
                    xalign 0.5
                    xfill True
                    yfill True

                    mousewheel True
                    draggable True

                    vbox:
                        for repo in repos:
                            textbutton repo["name"] action ([
                                SetDict(persistent._fom_autosave_config_github, "repo_name", repo["name"]),
                                Hide("fom_autosave_settings__repo_select")
                            ])

                vbar value YScrollValue("repos")

        hbox:
            xalign 0.5
            spacing 10

            textbutton _("Back"):
                action Hide("fom_autosave_settings__repo_select")
                sensitive promise.is_complete()

screen fom_autosave_settings__force_save():
    default promise = store._fom_autosave_task.AsyncTask(store._fom_autosave_github.backup_service.upload, "force save")

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

    use fom_autosave_screens__confirm(xmaximum=400, ymaximum=200, spacing=30):
        style_prefix "confirm"

        text _("Force save"):
            style "confirm_prompt"
            xalign 0.5

        if not promise.is_complete():
            text _("Saving..."):
                xalign 0.5
                text_align 0.5
        elif error is not None:
            text _("Failed to save. Check logs."):
                xalign 0.5
                text_align 0.5
        else:
            text _("Saved!"):
                xalign 0.5
                text_align 0.5

        hbox:
            xalign 0.5
            spacing 10

            textbutton _("Back"):
                action Hide("fom_autosave_settings__force_save")
                sensitive promise.is_complete()

screen fom_autosave_settings__slider(title, value, display, tooltip):
    $ tooltip_disp = renpy.get_screen("submods", "screens").scope["tooltip"]
    hbox spacing 10:
        text title
        bar value value style "slider_slider" xsize 200:
            hovered SetField(tooltip_disp, "value", tooltip)
            unhovered SetField(tooltip_disp, "value", tooltip_disp.default)
        text display
