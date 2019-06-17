
# Standard
import tkinter as tk
from tkinter import filedialog


# This project
import util.env as env
import util.misc as util


# Name of environment variable for tung install directory
__TUNG_DIR_VAR = 'tungdir'


# [TODO] Better checks needed here
def __valid_tung_dir(path):
    if path == None:
        return False
    return True


# Get tung install directory
def get_install_dir():
    tungDir = env.get_var(__TUNG_DIR_VAR)
    while not __valid_tung_dir(tungDir):
        tungDir = filedialog.askdirectory(title = 'Where is TUNG installed?')

    env.set_var(__TUNG_DIR_VAR, tungDir)
    return tungDir


def find_file(name):
    return util.find_file(name, get_install_dir())
