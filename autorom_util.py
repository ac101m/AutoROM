#!/usr/bin/env python3


# standard
import os
import sys


# Simple true/false prompt
def yes_no_prompt(prompt, default = 'n'):
    char = default
    print(prompt + '[y/n]:', end = '')
    sys.stdout.flush()
    while 1:
        c = sys.stdin.read(1)
        if c == '\n':
            if char == 'n' or char == 'N':
                return False
            elif char == 'y' or char == 'N':
                return True
            else:
                print(prompt + '[y/n]:', end = '')
                sys.stdout.flush()
        else:
            char = c


# Find a file within a directory with a given name
def find_file(fileName, dir):
    for root, dirs, files in os.walk(dir):
        for file in files:
            if os.path.basename(file) == fileName:
                return os.path.join(root, file)
    return None