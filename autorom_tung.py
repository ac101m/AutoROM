#!/usr/bin/env python3


# Standard
import tkinter as tk
from tkinter import filedialog


# This project
import autorom_env as env
import autorom_util as util


# Name of environment variable for tung install directory
__TUNG_DIR_VAR = 'tungdir'


# [TODO] Better checks needed here
def __valid_tung_dir(path):
    return True


# Get tung install directory
def get_install_dir():
    if env.get_var(__TUNG_DIR_VAR) != None:
        return env.get_var(__TUNG_DIR_VAR)
    else:
        while True:
            tungdir = filedialog.askdirectory(title = 'Where is TUNG installed?')
            if __valid_tung_dir(tungdir):
                env.set_var(__TUNG_DIR_VAR, tungdir)
                return tungdir


def find_file(name):
    return util.find_file(name, get_install_dir())
