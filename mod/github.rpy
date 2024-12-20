init -99 python in _fom_autosave_github:
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

        return request(http_method, github_api_url, request_headers, payload_json)

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
