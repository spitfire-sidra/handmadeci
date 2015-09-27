# -*- coding: utf-8 -*-
import os

from flask import Flask
from flask import json
from flask import request

import config
from tasks import code_review

app = Flask(__name__)
app.debug = config.DEBUG
app.secret_key = config.FLASK_SESSION_SECRET_KEY
app.root_path = os.path.abspath(os.path.dirname(__file__))


@app.route("/payload", methods=["POST"])
def payload():

    if request.method != "POST":
        return ""

    json_dict = json.loads(request.data)

    if "pull_request" in json_dict:
        # pull request related info
        br = json_dict["pull_request"]["head"]["ref"]
        commit_id = json_dict["pull_request"]["head"]["sha"]
        clone_url = json_dict["pull_request"]["head"]["repo"]["clone_url"]
        review_comments_api = json_dict["pull_request"]["review_comments_url"]
        pull_request_id = json_dict["number"]
        default_br = json_dict["repository"]["default_branch"]

        code_review.delay(
            clone_url,
            pull_request_id,
            br,
            review_comments_api,
            commit_id,
            default_br
        )

    return ""


if __name__ == "__main__":
    port = int(os.environ.get("PORT", config.PORT_NUMBER))
    app.run(host="0.0.0.0", port=port, debug=config.DEBUG)
