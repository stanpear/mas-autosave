init -980 python hide:
    import store
    import os

    script_dir = store.fom_getScriptDir(fallback="game/Submods/Autosave")
    script_dir = renpy.config.basedir + "/" + script_dir
    os.environ["SSL_CERT_FILE"] = script_dir + "/misc/cacert.pem"

init -100 python in _fom_autosave_http:
    import sys
    import json

    if sys.version_info.major == 2: # Python v2 only
        import urllib2

        def request(method, url, headers=None, body=None):
            req = urllib2.Request(url, data=body)
            req.get_method = lambda: method

            if headers is None:
                headers = {}
            for k, v in headers.items():
                req.add_header(k, v)

            opener = urllib2.build_opener(urllib2.HTTPHandler)
            res = opener.open(req)
            status = res.getcode()
            res_body = res.read()

            return status, res_body
