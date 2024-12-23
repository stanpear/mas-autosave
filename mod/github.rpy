init -997 python in _fom_autosave_github:
    from store._fom_autosave_http import request
    import json
    import base64

    def call_method(http_method, method_path, token=None, payload=None):
        github_api_url = "https://api.github.com{method_path}".format(method_path=method_path)
        request_headers = {
            "User-Agent": "Monika After Story v{version}".format(version=renpy.config.version),
            "Accept": "application/json"
        }

        if payload is not None:
            request_headers["Content-Type"] = "application/vnd.github.v3+json"
            payload_json = json.dumps(payload)
        else:
            payload_json = None

        if token is not None:
            request_headers["Authorization"] = "Bearer {token}".format(token=token)

        status, body = request(http_method, github_api_url, request_headers, payload_json)
        return (status, json.loads(body))

    def commit_file(file_path, repo_path, repo_owner, repo_name, committer_name, committer_email, commit_message, token):
        github_api_url = "/repos/{owner}/{repo}/contents/{repo_path}".format(owner=repo_owner, repo=repo_name, repo_path=repo_path)

        with open(file_path, "rb") as f:
            file_data = base64.b64encode(f.read())

        return call_method("PUT", github_api_url, token, {
            "content": file_data,
            "message": commit_message,
            "committer": {
                "name": committer_name,
                "email": committer_email
            }
        })

    def get_self(token):
        return call_method("GET", "/user", token)


init -980 python in _fom_autosave_github:
    from store._fom_autosave_config import has_remote_config, get_remote_config, set_remote_config
    from store.mas_threading import MASAsyncWrapper

    REMOTE_KEY = "github"
    OAUTH2_LINK = "https://oauth.mon.icu/authorize/github?scope=repo"

    if not has_remote_config(REMOTE_KEY):
        set_remote_config(REMOTE_KEY, {
            "oauth_token": "",
            "user_login": "",
            "user_name": "",
            "user_email": "",
            "repository": ""
        })

    def save_token_user_data(token, user):
        config = get_remote_config(REMOTE_KEY)
        config["oauth_token"] = token
        config["user_login"] = user["login"]
        config["user_name"] = user.get("name", None) or user["login"]
        config["user_email"] = user["email"]


    class TokenCheckTask(object):
        def __init__(self, token):
            self._token = token
            self._promise = None
            self._result = None
            self._error = None

        def run_in_background(self):
            self._promise = MASAsyncWrapper(self._execute)
            self._promise.start()

        def is_complete(self):
            return self._promise is not None and self._promise.done()

        def get(self):
            if not self.is_complete():
                raise RuntimeError("Task is still pending.")
            if self._error is not None:
                raise self._error
            return self._result

        def _execute(self):
            try:
                status, body = get_self(self._token)
                self._result = (status, body)
            except Exception as e:
                self._error = e


screen fom_autosave_settings_github_options():
    default config = store._fom_autosave_config.get_remote_config(store._fom_autosave_github.REMOTE_KEY)

    hbox spacing 5:
        if config.get("user_name", None):
            text _("Authorized as {0} {{color=#22c55e}}[[OK]{{/color}}".format(config["user_name"]))

        textbutton _("Authorize with Github"):
            style "check_button"
            action Show("fom_autosave_settings_github_oauth2")

    hbox spacing 10:
        textbutton _("Select repository"):
            style "check_button"
            action NullAction()

screen fom_autosave_settings_github_oauth2():
    style_prefix "confirm"
    modal True
    zorder 200
    add mas_getTimeFile("gui/overlay/confirm.png")

    frame:
        vbox:
            xmaximum 500
            xfill True

            align (0.5, 0.5)
            spacing 30

            text _("Authorize with Github"):
                style "confirm_prompt"
                xalign 0.5

            vbox spacing 10:
                text _("Click the 'Authorize' button below to begin. When ready, "
                    "click the 'Paste' button to save access token."):
                    xalign 0.5
                    text_align 0.5

                text _("{size=-8}Your token {i}is not{/i} shared with anyone "
                    "and is not stored anywhere except your computer.{/size}"):
                    xalign 0.5
                    text_align 0.5

            hbox:
                xalign 0.5
                spacing 10

                textbutton _("Cancel"):
                    action Hide("fom_autosave_settings_github_oauth2")

                textbutton _("Authorize"):
                    action OpenURL(store._fom_autosave_github.OAUTH2_LINK)

                textbutton _("Paste"):
                    action Show("fom_autosave_settings_github_token_check")

screen fom_autosave_settings_github_token_check():
    default config = store._fom_autosave_config.get_remote_config(store._fom_autosave_github.REMOTE_KEY)
    default token = pygame.scrap.get(pygame.SCRAP_TEXT)
    default task = store._fom_autosave_github.TokenCheckTask(token)

    timer 0.5 action Function(renpy.restart_interaction) repeat True
    on "show" action Function(task.run_in_background)

    default user = None
    default error = None

    python:
        if task.is_complete():
            try:
                status, body = task.get()
                user = body
            except Exception as e:
                user = None
                error = e

    style_prefix "confirm"
    modal True
    zorder 200
    add mas_getTimeFile("gui/overlay/confirm.png")

    frame:
        vbox:
            xmaximum 500
            xfill True

            align (0.5, 0.5)
            spacing 30

            text _("Authorize with Github"):
                style "confirm_prompt"
                xalign 0.5

            if not task.is_complete():
                text _("Verifying token..."):
                    xalign 0.5
                    text_align 0.5

            elif user is not None:
                text _("Authorized as {0}".format(user.get("name", None) or user["login"])):
                    xalign 0.5
                    text_align 0.5

            elif error is not None:
                text _("Failed to authorize"):
                    xalign 0.5
                    text_align 0.5

            hbox:
                xalign 0.5
                spacing 10

                textbutton _("OK"):
                    sensitive task.is_complete()
                    action If(
                        user is not None,
                        true=[Function(store._fom_autosave_github.save_token_user_data, token, user),
                              Hide("fom_autosave_settings_github_token_check"),
                              Hide("fom_autosave_settings_github_oauth2")],
                        false=Hide("fom_autosave_settings_github_token_check")
                    )
