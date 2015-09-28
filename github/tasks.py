# -*- coding: utf-8 -*-
import os
import shutil
from urlparse import urlparse

from helpers.git import GitHelper
from helpers.taskqueue import get_task_queue
from linters.flake8 import get_flake8_result
from lib.api import post_comment


TASK_QUEUE = get_task_queue()
GIT = GitHelper()


@TASK_QUEUE.task
def code_review(clone_url, pull_request_id, br, review_comments_api, commit_id, default_br="master"):

    # go to workspace first
    workspace_path = os.path.join(os.getcwd(), "workspace")
    if os.path.exists(workspace_path) and os.path.isdir(workspace_path):
        os.chdir(workspace_path)
    elif not os.path.exists(workspace_path):
        shutil.makedirs(workspace_path)
    else:
        raise EnvironmentError("path: {0} is not a folder".format(workspace_path))

    GIT.clone(clone_url)

    # go to the repo
    path = urlparse(clone_url).path
    os.chdir(path.split("/")[-1][:-4])

    GIT.fetch_qull_request(pull_request_id, br)
    GIT.checkout(br)

    remote_default_br = "origin/{0}".format(default_br)
    changed_files = GIT.get_changed_files(remote_default_br)

    for f in changed_files:
        comment_tuples = get_flake8_result(f)
        for c in comment_tuples:
            post_comment(review_comments_api, commit_id, f, int(c[0]), c[1])

    # cleanup
    GIT.checkout("master")
    GIT.delete_branch(br)
