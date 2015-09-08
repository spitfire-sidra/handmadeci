#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import logging
import subprocess

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def get_changed_file_paths():

    stdout_str = subprocess.check_output([
        'git',
        '--no-pager',
        'diff',
        '--no-color',
        '--name-status',
        '--diff-filter=AMRT',
        '--ignore-space-at-eol',
        'HEAD~',
        'src/'
    ])

    file_path_regex = re.compile(r'^.\s+(?P<file_path>.+)')

    file_paths = []

    stdout_lines = stdout_str.split('\n')
    for line in stdout_lines:
        match_obj = file_path_regex.search(line)
        if match_obj:
            file_paths.append(match_obj.group('file_path'))

    return file_paths


def get_testcase_path(file_path):

    testcase_path = os.path.join('test', 'test_{}'.format(os.path.basename(file_path)))
    if os.path.exists(testcase_path) and os.path.isfile(testcase_path):
        return testcase_path

    return ''


def main():
    changed_file_paths = get_changed_file_paths()

    testcase_paths = []
    for file_path in changed_file_paths:
        testcase_path = get_testcase_path(file_path)

        if not testcase_path:
            logging.warning('No testcase for {}'.format(file_path))
            continue

        testcase_paths.append(testcase_path)

    if testcase_paths:
        subprocess.call(['py.test'] + testcase_paths)


if __name__ == '__main__':
    main()
