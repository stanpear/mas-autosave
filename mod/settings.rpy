default persistent._fom_autosave_config_common = None
default persistent._fom_autosave_config_github = None

init -1000 python:
    if persistent._fom_autosave_config_common is None:
        persistent._fom_autosave_config_common = {
            "backup_freq": 1,
            "on_exit": False
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


screen fom_autosave_settings():
    $ tooltip_disp = renpy.get_screen("submods", "screens").scope["tooltip"]
    $ github_api_key = mas_getAPIKey(store._fom_autosave_config.KEY_ID_GITHUB)
    $ repo_name = persistent._fom_autosave_config_github.get("repo_name", None)
    $ backup_service = store._fom_autosave_common.SELECTED_BACKUP(reason=_("forced save"))

    vbox:
        style_prefix "check"
        xmaximum 800
        xfill True

        text _("Feeling confused and need help setting up? {b}Click {a=https://github.com/Friends-of-Monika/mas-autosave?tab=readme-ov-file#-configuring}here{/a}.{/b}")

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

        hbox:
            use fom_autosave_settings__slider(
                title=_("Backup frequency"),
                value=DictValue(persistent._fom_autosave_config_common, "backup_freq", offset=0, range=len(store._fom_autosave_timer.BACKUP_FREQ) - 1),
                display=store._fom_autosave_timer.BACKUP_FREQ[persistent._fom_autosave_config_common["backup_freq"]][0],
                tooltip=_("You can set automatic backup frequency by adjusting this slider."))

            textbutton _("Save on goodbye"):
                selected persistent._fom_autosave_config_common["on_exit"]
                action ToggleDict(persistent._fom_autosave_config_common, "on_exit")
                hovered SetField(tooltip_disp, "value", _("You can toggle automatic backup on 'Goodbye' by clicking here."))
                unhovered SetField(tooltip_disp, "value", tooltip_disp.default)

        hbox:
            textbutton _("Force save"):
                sensitive github_api_key and repo_name
                action Show("fom_autosave_settings__force_save", None, backup_service)
                hovered SetField(tooltip_disp, "value", _("Click to force save the persistent to Github."))
                unhovered SetField(tooltip_disp, "value", tooltip_disp.default)
                xoffset -22

            textbutton _("Load persistent"):
                sensitive github_api_key and repo_name
                action Show("fom_autosave_settings__commit_select")
                hovered SetField(tooltip_disp, "value", _("Click to select saved persistent to load."))
                unhovered SetField(tooltip_disp, "value", tooltip_disp.default)
                xoffset -32

screen fom_autosave_settings__repo_select():
    default github_api_key = mas_getAPIKey(store._fom_autosave_config.KEY_ID_GITHUB)
    default promise = store._fom_autosave_task.AsyncTask(store._fom_autosave_github.get_own_repos, github_api_key)

    timer 0.5 action Function(renpy.restart_interaction) repeat True
    on "show" action Function(promise.run_in_background)
    modal True
    zorder 200

    default back_action = Hide("fom_autosave_settings__repo_select")

    default repos = None
    default error = None

    python:
        try:
            if promise.is_complete():
                status, repos = promise.get()
        except Exception as e:
            if error is None:
                store._fom_autosave_logging.logger.error(_("Failed to load repositories: {0}"), e)
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
                                SetDict(persistent._fom_autosave_config_github, "repo_owner", repo["owner"]["login"]),
                                SetDict(persistent._fom_autosave_config_github, "repo_name", repo["name"]),
                                Hide("fom_autosave_settings__repo_select")
                            ])

                vbar value YScrollValue("repos")

        hbox:
            xalign 0.5
            spacing 10

            textbutton _("Back"):
                action back_action
                sensitive promise.is_complete()

    if promise.is_complete():
        key "K_ESCAPE" action back_action

screen fom_autosave_settings__force_save(backup_service):
    default promise = store._fom_autosave_task.AsyncTask(backup_service.upload)

    timer 0.5 action Function(renpy.restart_interaction) repeat True
    on "show" action Function(promise.run_in_background)
    modal True
    zorder 200

    default ok_action = Hide("fom_autosave_settings__force_save")

    default error = None

    python:
        try:
            if promise.is_complete():
                promise.get()
        except Exception as e:
            if error is None:
                store._fom_autosave_logging.logger.error(_("Failed to upload save: {0}"), e)
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
                action ok_action
                sensitive promise.is_complete()

    if promise.is_complete():
        key "K_ESCAPE" action ok_action
        key "K_RETURN" action ok_action

screen fom_autosave_settings__slider(title, value, display, tooltip):
    $ tooltip_disp = renpy.get_screen("submods", "screens").scope["tooltip"]
    hbox spacing 10:
        text title
        bar value value style "slider_slider" xsize 200:
            hovered SetField(tooltip_disp, "value", tooltip)
            unhovered SetField(tooltip_disp, "value", tooltip_disp.default)
        text display

screen fom_autosave_settings__commit_select():
    default github_api_key = mas_getAPIKey(store._fom_autosave_config.KEY_ID_GITHUB)
    default backup_service = store._fom_autosave_common.SELECTED_BACKUP(None)
    default promise = store._fom_autosave_task.AsyncTask(store._fom_autosave_github.list_commits,
        repo_owner=persistent._fom_autosave_config_github["repo_owner"],
        repo_name=persistent._fom_autosave_config_github["repo_name"],
        repo_path="persistent",
        token=github_api_key)

    timer 0.5 action Function(renpy.restart_interaction) repeat True
    on "show" action Function(promise.run_in_background)
    modal True
    zorder 200

    default back_action = Hide("fom_autosave_settings__commit_select")

    default commits = None
    default error = None

    python:
        try:
            if promise.is_complete():
                status, commits = promise.get()
        except Exception as e:
            if error is None:
                store._fom_autosave_logging.logger.error(_("Failed to load saves: {0}"), e)
                error = e

    use fom_autosave_screens__confirm(xmaximum=800, ymaximum=400, spacing=30):
        style_prefix "confirm"

        text _("Load persistent"):
            style "confirm_prompt"
            xalign 0.5

        if not promise.is_complete():
            text _("Loading..."):
                xalign 0.5
                text_align 0.5

        elif error is not None:
            text _("Failed to load saves. Check logs."):
                xalign 0.5
                text_align 0.5

        else:
            hbox:
                viewport id "commits":
                    xalign 0.5
                    xfill True
                    yfill True

                    mousewheel True
                    draggable True

                    vbox spacing 10:
                        for commit in commits:
                            $ commit_name = commit["commit"]["message"]
                            $ commit_date = commit["commit"]["author"]["date"]
                            $ commit_sha = commit["sha"]

                            vbox:
                                textbutton "[commit_name!q]" action ([
                                    Hide("fom_autosave_settings__commit_select"),
                                    SetField(backup_service, "commit", commit_sha),
                                    Show("fom_autosave_settings__load_commit", None, backup_service)])
                                text _("{size=-6}Uploaded at [commit_date]{/size}") xoffset 5
                                text "{size=-10}[commit_sha]{/size}" xoffset 5

                vbar value YScrollValue("commits")

        hbox:
            xalign 0.5
            spacing 10

            textbutton _("Back"):
                action back_action
                sensitive promise.is_complete()

    if promise.is_complete():
        key "K_ESCAPE" action back_action

screen fom_autosave_settings__load_commit(backup_service):
    default promise = store._fom_autosave_task.AsyncTask(backup_service.download)

    timer 0.5 action Function(renpy.restart_interaction) repeat True
    on "show" action Function(promise.run_in_background)
    modal True
    zorder 200

    default ok_action = [SetField(renpy.persistent, "should_save_persistent", False), Quit(confirm=False)]
    default back_action = Hide("fom_autosave_settings__load_commit")

    default error = None

    python:
        try:
            if promise.is_complete():
                promise.get()
        except Exception as e:
            if error is None:
                store._fom_autosave_logging.logger.error(_("Failed to load persistent: {0}"), e)
                error = e

    use fom_autosave_screens__confirm(xmaximum=500, ymaximum=200, spacing=30):
        style_prefix "confirm"

        text _("Load persistent"):
            style "confirm_prompt"
            xalign 0.5

        if not promise.is_complete():
            text _("Loading..."):
                xalign 0.5
                text_align 0.5
        elif error is not None:
            text _("Failed to load persistent. Check logs.\n"
                   "{i}Your current persistent was not overwritten.{/i}"):
                xalign 0.5
                text_align 0.5
        else:
            text _("Persistent loaded.\n"
                   "The game needs to be restarted now."):
                xalign 0.5
                text_align 0.5

        hbox:
            xalign 0.5
            spacing 10

            if not promise.is_complete() or error is not None:
                textbutton _("Back"):
                    action back_action
                    sensitive promise.is_complete()
            else:
                textbutton _("Restart"):
                    action ok_action
                    sensitive promise.is_complete()

    if not promise.is_complete() or error is not None:
        key "K_ESCAPE" action back_action
    else:
        key "K_RETURN" action ok_action
