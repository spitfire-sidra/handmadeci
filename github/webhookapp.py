# -*- coding: utf-8 -*-
import os

import config


app = Flask(__name__)
app.debug = config.DEBUG
app.secret_key = config.FLASK_SESSION_SECRET_KEY
app.root_path = os.path.abspath(os.path.dirname(__file__))


@app.route('/webhook', methods=['POST'])
def webhook():

    if request.method == 'POST':
        json_content = json.loads(request.data)
        if 'pull_request' in json_content:
            api_url = json_content['pull_request']['url']
            prid = json_content['number']
            changed_files = json_content['pull_request']['changed_files']
            patch_url = json_content['pull_request']['patch_url']
            default_branch = json_content['repository']['default_branch']
            clone_url = json_content['pull_request']['head']['repo']['clone_url']
            commit_id = json_content['pull_request']['head']['sha']
            branch = json_content['pull_request']['head']['ref']
            linter.delay(clone_url,prid,branch, json_content['pull_request']['review_comments_url'], commit_id)

    return ''


if __name__ == "__main__":
    port = int(os.environ.get('PORT', config.PORT_NUMBER))
    app.run(host='0.0.0.0', port=port, debug=config.DEBUG)
