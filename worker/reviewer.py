# -*- coding: utf-8 -*-
import re
import os
import subprocess
from urlparse import urlparse

def main(url, prid, branch):
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
                print line_no, comment.strip()

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

if __name__ == '__main__':
    main('https://github.com/spitfire-sidra/handmadeci.git', 1, 'webhook-worker')
