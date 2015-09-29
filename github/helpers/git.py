# -*- coding: utf-8 -*-
import re
import subprocess

from pipes import quote


class GitHelper(object):

    @classmethod
    def clone(cls, repo):

        try:
            subprocess.call(['git', 'clone', quote(repo)])
        except subprocess.CalledProcessError as e:
            if 'already exists and is not an empty directory' in e.stderr:
                pass

    @classmethod
    def checkout(cls, br):
        subprocess.call(['git', 'checkout', quote(br)])

    @classmethod
    def get_changed_files(cls, br):
        output = subprocess.check_output([
            'git',
            '--no-pager',
            'diff',
            '--no-color',
            '--name-status',
            '--diff-filter=AMRT',
            '--ignore-space-at-eol',
            quote(br),
        ])

        changed_file_set = set()
        changed_file_re = re.compile(r'^.\s+(?P<changed_file>.+)')
        for line in output.split('\n'):
            match = changed_file_re.search(line)
            if match:
                changed_file_set.add(match.group('changed_file'))

        return list(changed_file_set)

    @classmethod
    def fetch_pull_request(cls, pull_request_id, br):
        subprocess.call([
            'git',
            'fetch',
            'origin',
            'pull/{0}/head:{1}'.format(pull_request_id, quote(br))
        ])

    @classmethod
    def delete_branch(cls, br):
        subprocess.call(['git', 'branch', '-D', quote(br)])
