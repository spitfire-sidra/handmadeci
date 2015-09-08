#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import subprocess


def get_changed_files():

    stdout_str = subprocess.check_output([
        'git',
        '--no-pager',
        'diff',
        '--no-color',
        '--name-status',
        '--diff-filter=AMRT',
        '--ignore-space-at-eol',
        'HEAD~'
    ])

    file_path_regex = re.compile(r'^.\s+(?P<file_path>.+)')
    stdout_lines = stdout_str.split('\n')

    for line in stdout_lines:
        match_obj = file_path_regex.search(line)
        if match_obj:
            print match_obj.group('file_path')


if __name__ == '__main__':
    get_changed_files()
