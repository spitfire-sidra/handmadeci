#!/usr/bin/env python
# -*- coding: utf-8 -*-
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


if __name__ == '__main__':
    get_changed_files()
