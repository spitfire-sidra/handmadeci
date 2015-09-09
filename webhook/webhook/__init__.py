# -*- coding: utf-8 -*-
import os

from flask import Flask
from flask import json
from flask import jsonify
from flask import request
from flask import render_template

from webhook import config


app = Flask(__name__)
app.debug = config.DEBUG
app.secret_key = config.FLASK_SESSION_SECRET_KEY
app.root_path = os.path.abspath(os.path.dirname(__file__))


@app.route('/webhook', methods=['POST'])
def webhook():

    if request.method == 'POST':
        json_content = json.loads(request.data)
        if 'pull_request' in json_content:
            url = json_content['pull_request']['url']
            changed_files = json_content['pull_request']['changed_files']
            patch_url = json_content['patch_url']
            default_branch = json_content['repository']['default_branch']
            print url
            print changed_files
            print patch_url
            print default_branch

    return ''
