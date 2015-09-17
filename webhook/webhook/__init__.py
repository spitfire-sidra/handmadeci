# -*- coding: utf-8 -*-
import re
import json
import os
import subprocess
from urlparse import urlparse

import requests
from requests.auth import HTTPBasicAuth
from celery import Celery
import iron_celery

from flask import Flask
from flask import json
from flask import jsonify
from flask import request
from flask import render_template

from webhook import config
from webhook import account

token = ""
project_id = ""
BROKER_URL = 'ironmq://{}:{}@?connect_timeout=20'.format(project_id, token)
CELERY_RESULT_BACKEND = 'ironcache:://{}:{}'.format(project_id, token)
#celery = Celery('mytasks', broker=BROKER_URL, backend='ironcache://')

celery = Celery('handmadeci', broker=BROKER_URL, backend=CELERY_RESULT_BACKEND)

app = Flask(__name__)
app.debug = config.DEBUG
app.secret_key = config.FLASK_SESSION_SECRET_KEY
app.root_path = os.path.abspath(os.path.dirname(__file__))


def leave_comment(api, commit_id, path, pos, comment):
    print api
    print commit_id
    print path
    print pos
    print comment
    r = requests.post(api, data=json.dumps({
        'body': comment,
        'commit_id': commit_id,
        'position': pos,
        'path': path,
        }),
        auth=HTTPBasicAuth(account.user, account.passwd)
    )
    print r.content

@celery.task
def linter(url, prid, branch, api, commit_id):
    try:
        subprocess.call([
            'git',
            'clone',
            url
        ])
    except subprocess.CalledProcessError as e:
        if 'already exists and is not an empty directory' in e.stderr:
            pass

    path = urlparse(url).path
    print path
    print path.split('/')[-1][:-4]
    os.chdir(path.split('/')[-1][:-4])

    stdout_str = subprocess.check_output([
        'git',
        'fetch',
        'origin',
        'pull/{0}/head:{1}'.format(prid, branch)
    ])

    stdout_str = subprocess.check_output([
        'git',
        'checkout',
        branch
    ])

    stdout_str = subprocess.check_output([
        'git',
        '--no-pager',
        'diff',
        '--no-color',
        '--name-status',
        '--diff-filter=AMRT',
        '--ignore-space-at-eol',
        'origin/master',
    ])
    print stdout_str

    file_path_regex = re.compile(r'^.\s+(?P<file_path>.+)')

    file_paths = []

    stdout_lines = stdout_str.split('\n')
    for line in stdout_lines:
        match_obj = file_path_regex.search(line)
        if match_obj:
            file_paths.append(match_obj.group('file_path'))
            try:
                stdout_str = subprocess.check_output([
                    'flake8',
                    match_obj.group('file_path'),
                ],
                stderr=subprocess.STDOUT
                )
            except subprocess.CalledProcessError as e:
                stdout_str = e.output

            lines = stdout_str.split('\n')
            for line in lines:
                if not line:
                    continue
                f, line_no, __, comment = line.split(':')
                #leave_comment(api, commit_id, path, pos, comment)
                leave_comment(api, commit_id, f, int(line_no), comment.strip())

    subprocess.call([
        'git',
        'checkout',
        'master' # default branch
    ])

    subprocess.call([
        'git',
        'branch',
        '-D',
        branch
    ])


    pass

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
            print api_url
            print prid
            print changed_files
            print patch_url
            print default_branch
            print clone_url
            print branch
            print commit_id
            linter.delay(clone_url,prid,branch, json_content['pull_request']['review_comments_url'], commit_id)

    return ''
