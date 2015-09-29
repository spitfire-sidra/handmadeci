# -*- coding: utf-8 -*-
import re
import subprocess

from pipes import quote


def get_flake8_result(file_path):

    try:
        output = subprocess.check_output(["flake8", quote(file_path)], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        # flake8 prints result to stderr
        output = e.output

    result_tuples = []
    lint_re = re.compile(r"(?P<file>\w+):(?P<pos>\d+):(:?\d+):\s(?P<lint>\w+)")
    for line in output.split("\n"):
        if not line:
            continue

        match = lint_re.search(line)
        if match:
            result_tuples.append((match.group("pos"), match.group("lint")))

    return result_tuples
