# -*- coding: utf-8 -*-
import requests
from flask import json

import config


_HEADERS = {
    'Authorization': 'token {0}'.format(config.GITHUB_ACCESS_TOKEN),
}


def post_comment(api, commit_id, path, pos, comment):
    resp = requests.post(
        api,
        data=json.dumps({
            'commit_id': commit_id,
            'path': path,
            'position': pos,
            'body': comment,
        }),
        headers=_HEADERS
    )

    if config.DEBUG:
        print api
        print commit_id
        print path
        print pos
        print comment
        print _HEADERS
        print resp.content
