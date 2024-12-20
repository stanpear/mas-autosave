init -99 python in _fom_autosave_github:
    from store._fom_autosave_http import request
    import json

    def call_method(http_method, method_path, token=None, payload=None):
        github_api_url = "https://api.github.com{method_path}".format(method_path=method_path)
        request_headers = {
            "User-Agent": "Monika After Story v{version}".format(version=renpy.config.version)
        }

        if payload is not None:
            payload_json = json.dumps(payload)
            request_headers["Content-Type"] = "application/vnd.github+json"
        else:
            payload_json = None

        if token is not None:
            request_headers["Authorization"] = "Bearer {token}".format(token=token)

        return request(http_method, github_api_url, header, payload_json)
