default persistent._fom_autosave_config_github = None

init -1000 python:
    if persistent._fom_autosave_config_github is None:
        persistent._fom_autosave_config_github = {
            "repo_name": ""
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
    vbox:
        style_prefix "check"
        xmaximum 800
        xfill True

        hbox:
            $ github_api_key = mas_getAPIKey(store._fom_autosave_config.KEY_ID_GITHUB)
            if github_api_key:
                text _("- API token {color=#84cc16}is set{/color}")
            else:
                text _("- API token {color=#ef4444}is not set{/color}")

            textbutton _("Open API keys menu"):
                action Show("mas_apikeys")
                xoffset -12

        hbox:
            $ repo_name = persistent._fom_autosave_config_github.get("repo_name", None)
            if repo_name:
                text _("- Repository {color=#84cc16}is set{/color}{space=10}([repo_name])")
            else:
                text _("- Repository {color=#ef4444}is not selected{/color}")

            textbutton _("Select repository"):
                action Show("fom_autosave_settings__repo_select")
                sensitive bool(github_api_key)
                xoffset -12

screen fom_autosave_settings__repo_select():
    default github_api_key = mas_getAPIKey(store._fom_autosave_config.KEY_ID_GITHUB)
    default promise = store._fom_autosave_task.AsyncTask(store._fom_autosave_github.get_own_repos, github_api_key)

    timer 0.5 action Function(renpy.restart_interaction) repeat True
    on "show" action Function(promise.run_in_background)

    $ repos = None
    $ error = None

    python:
        try:
            if promise.is_complete():
                status, body = promise.get()
                repos = body
        except Exception as e:
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
