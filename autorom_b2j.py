#!/usr/bin/env python3


#standard
import os
import platform
import subprocess
import sys
import shutil
import zipfile
import urllib.request


# this project
import autorom_util as util
import autorom_b2j_md5 as md5
import autorom_tung as tung


# Where to find board to json
__B2J_URL = 'https://github.com/Stenodyon/BoardToJson/releases/download/1.0/BoardToJson.zip'
__B2J_DIR = os.path.dirname(__file__) + '/BoardToJson/'


# Return true if boardtojson is present
# more comprehensive checks can be implemented later if need be
def installed():
    if os.path.exists(__B2J_DIR):
        if os.path.isdir(__B2J_DIR):
            if len(os.listdir(__B2J_DIR)) != 0:
                return True
    return False


# Install boardtojson
def install():
    if not os.path.exists(__B2J_DIR):
        os.mkdir(__B2J_DIR)

    # Download board to json binaries
    b2jZipPath = __B2J_DIR + '/b2j.zip'
    urllib.request.urlretrieve(__B2J_URL, b2jZipPath)

    # Check file hashes against known good md5 checksums
    if md5.check(b2jZipPath):
        print("Oshit son! looks like these binaries might be dodgy!")
        if not util.yes_no_prompt('Continue? '):
            print('B2J install failed, quitting')
            uninstall()
            sys.exit()

    # Decompress the zip
    zip = zipfile.ZipFile(b2jZipPath, 'r')
    zip.extractall(__B2J_DIR)
    zip.close()

    # Prompt user for TUNG install path
    tungAsmFile = 'Assembly-CSharp.dll'
    tungAsmPath = tung.find_file(tungAsmFile)
    if tungAsmPath == None:
        print('ERROR, unable to locate ' + tungAsmFile)
        print('B2J install failed, quitting')
        uninstall()
        sys.exit()
    else:
        print('Located game assembly at ' + tungAsmPath)
        shutil.copyfile(tungAsmPath, __B2J_DIR + tungAsmFile)
        print('B2J install successful!')

    # On linux, give execute permissions to B2J executable
    if platform.system() == 'Linux':
        command = ['chmod', '+x', __B2J_DIR + 'BoardToJson.exe']
        subprocess.call(command, shell = False)


# Deletes the b2j dir and everything therein
# if for some reason B2J_DIR points at a file, get rid of that too
def uninstall():
    if os.path.exists(__B2J_DIR):
        if os.path.isdir(__B2J_DIR):
            shutil.rmtree(__B2J_DIR)
        else:
            os.remove(__B2J_DIR)


# convert tung board to json
def board_to_json(boardPath, jsonPath):
    command = [__B2J_DIR + 'BoardToJson.exe', '-i', boardPath, '-o', jsonPath]
    subprocess.call(command, shell = False, stdout = subprocess.DEVNULL)


# convert json to tung board
def json_to_board(jsonPath, boardPath):
    command = [__B2J_DIR + 'BoardToJson.exe', '-i', jsonPath, '-o', boardPath]
    subprocess.call(command, shell = False, stdout = subprocess.DEVNULL)
