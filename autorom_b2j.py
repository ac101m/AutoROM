#!/usr/bin/env python3


#standard
import os
import subprocess
import sys
import shutil
import zipfile
import tkinter as tk
from tkinter import filedialog
import urllib.request


# this project
from autorom_utils import *
from autorom_b2j_md5 import *


# Where to find board to json
B2J_URL = 'https://github.com/Stenodyon/BoardToJson/releases/download/1.0/BoardToJson.zip'
B2J_DIR = os.path.dirname(__file__) + '/BoardToJson/'


# Return true if boardtojson is present
# more comprehensive checks can be implemented later if need be
def b2j_present():
    if os.path.exists(B2J_DIR):
        if os.path.isdir(B2J_DIR):
            if len(os.listdir(B2J_DIR)) != 0:
                return True
    return False


# Install boardtojson
def get_b2j():
    if not os.path.exists(B2J_DIR):
        os.mkdir(B2J_DIR)

    # Download board to json binaries
    b2jZipPath = B2J_DIR + '/b2j.zip'
    urllib.request.urlretrieve(B2J_URL, b2jZipPath)

    # Check file hashes against known good md5 checksums
    if b2j_md5_fail(b2jZipPath):
        print("Oshit son! looks like these binaries might be dodgy!")
        if not yes_no_prompt('Continue? '):
            print('B2J install failed, quitting')
            delete_b2j()
            sys.exit()

    # Decompress the zip
    zip_ref = zipfile.ZipFile(b2jZipPath, 'r')
    zip_ref.extractall(B2J_DIR)
    zip_ref.close()

    # Prompt user for TUNG install path
    tungAsmFile = 'Assembly-CSharp.dll'
    tungDir = filedialog.askdirectory(title = 'Where is TUNG installed?')
    tungAsmPath = find_file(tungAsmFile, tungDir)
    if tungAsmPath == '':
        print('ERROR, unable to locate ' + tungAsmFile)
        print('B2J install failed, quitting')
        delete_b2j()
        sys.exit()
    else:
        print('Located game assembly at ' + tungAsmPath)
        shutil.copyfile(tungAsmPath, B2J_DIR + tungAsmFile)
        print('B2J install successful!')


# Deletes b2j dir and everything therein
# if for some reason B2J_DIR points at a file, get rid of that too
def delete_b2j():
    if os.path.exists(B2J_DIR):
        if os.path.isdir(B2J_DIR):
            shutil.rmtree(B2J_DIR)
        else:
            os.remove(B2J_DIR)


# convert tung board to json
def board_to_json(boardPath, jsonPath):
    subprocess.run([B2J_DIR + 'BoardToJson.exe', '-i', boardPath, '-o', jsonPath])


# convert json to tung board
def json_to_board(jsonPath, boardPath):
    subprocess.run([B2J_DIR + 'BoardToJson.exe', '-i', jsonPath, '-o', boardPath])
