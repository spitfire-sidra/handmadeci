# -*- coding: utf-8 -*-
import requests
from requests.auth import HTTPBasicAuth


def leave_comment(api, commit_id, path, pos, comment):
    r = requests.post(api, data=json.dumps({
        'body': comment,
        'commit_id': commit_id,
        'position': pos,
        'path': path,
        }),
        auth=HTTPBasicAuth(account.user, account.passwd)
    )
    print r.content
