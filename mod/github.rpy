init -897 python in _fom_autosave_github:
    from store._fom_autosave_http import request
    from store._fom_autosave_common import PersistentBackup
    from store._fom_autosave_persistent import get_persistent_path

    from store import persistent
    import store

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

    def commit_file(file_path, repo_path, repo_owner, repo_name, commit_message, token):
        github_api_url = "/repos/{owner}/{repo}/contents/{repo_path}".format(
            owner=repo_owner,
            repo=repo_name,
            repo_path=repo_path)

        try:
            status, file_meta = get_file_metadata(repo_owner, repo_name, repo_path, token)
            if status != 200:
                raise ValueError("Unexpected status code {0} != 200".format(status))
            file_sha = file_meta["sha"]
        except Exception as e:
            file_sha = None

        with open(file_path, "rb") as f:
            file_data = base64.b64encode(f.read())

        params = {
            "content": file_data,
            "message": commit_message
        }

        if file_sha is not None:
            params["sha"] = file_sha

        return call_method("PUT", github_api_url, token, params)

    def get_file_metadata(repo_owner, repo_name, repo_path, token):
        github_api_url = "/repos/{owner}/{repo}/contents/{repo_path}".format(
            owner=repo_owner,
            repo=repo_name,
            repo_path=repo_path)
        return call_method("GET", github_api_url, token)

    def get_own_repos(token):
        return call_method("GET", "/user/repos", token)

    def get_self(token):
        return call_method("GET", "/user", token)


    class GithubBackup(PersistentBackup):
        def is_configured(self):
            token = store.mas_getAPIKey(store._fom_autosave_config.KEY_ID_GITHUB)
            commit_fmt = persistent._fom_autosave_config_github["commit_fmt"]
            repo_name=persistent._fom_autosave_config_github["repo_name"]
            return bool(token and commit_fmt and repo_name)

        def upload(self, reason):
            token = store.mas_getAPIKey(store._fom_autosave_config.KEY_ID_GITHUB)
            status, user_info = get_self(token)
            if status != 200:
                raise ValueError("Unexpected status code {0} != 200".format(status))

            commit_fmt = persistent._fom_autosave_config_github["commit_fmt"]
            commit_message = renpy.substitute(commit_fmt, {"reason": reason})

            per_path = get_persistent_path()
            status, commit = commit_file(
                file_path=per_path,
                repo_path="persistent",
                repo_owner=user_info["login"],
                repo_name=persistent._fom_autosave_config_github["repo_name"],
                commit_message=commit_message,
                token=token
            )

        def download(self):
            pass


    backup_service = GithubBackup()
