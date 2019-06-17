
# Standard
import os
import platform
import subprocess
import sys
import shutil
import zipfile
import urllib.request


# This project
import util.misc as util
import util.tung as tung


# Where to find board to json
__B2J_URL = 'https://github.com/Stenodyon/BoardToJson/releases/download/1.0/BoardToJson.zip'
__B2J_BIN_DIR = os.path.join(os.path.dirname(__file__), 'bin')


# Valid md5 strings for b2j.zip
__B2J_MD5 = ['e65eebceacdce2a976c6a8b4e6242aa3']


# Check if a file matches any of the above checksums
def check(path):
    fileMD5 = util.md5_hex_digest(path)
    for validMD5 in __B2J_MD5:
        if validMD5 == fileMD5:
            return False
    return True


# Return true if boardtojson is present
# more comprehensive checks can be implemented later if need be
def installed():
    if os.path.exists(__B2J_BIN_DIR):
        if os.path.isdir(__B2J_BIN_DIR):
            if len(os.listdir(__B2J_BIN_DIR)) != 0:
                return True
    return False


# Install boardtojson
def install():

    # Make directory if missing
    os.makedirs(__B2J_BIN_DIR, exist_ok = True)

    # Download board to json binaries
    b2jZipPath = os.path.join(__B2J_BIN_DIR, 'b2j.zip')
    urllib.request.urlretrieve(__B2J_URL, b2jZipPath)

    # Check file hashes against known good md5 checksums
    if check(b2jZipPath):
        print("Oshit son! looks like these binaries might be dodgy!")
        if not util.yes_no_prompt('Continue? '):
            print('B2J install failed, quitting')
            uninstall()
            sys.exit()

    # Decompress the zip
    zip = zipfile.ZipFile(b2jZipPath, 'r')
    zip.extractall(__B2J_BIN_DIR)
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
        shutil.copyfile(tungAsmPath, os.path.join(__B2J_BIN_DIR, tungAsmFile))
        print('B2J install successful!')

    # On linux, give execute permissions to B2J executable
    if platform.system() == 'Linux':
        executablePath = os.path.join(__B2J_BIN_DIR, 'BoardToJson.exe')
        command = ['chmod', '+x', executablePath]
        subprocess.call(command, shell = False)


# Deletes the b2j dir and everything therein
# if for some reason B2J_DIR points at a file, get rid of that too
def uninstall():
    if os.path.exists(__B2J_BIN_DIR):
        if os.path.isdir(__B2J_BIN_DIR):
            shutil.rmtree(__B2J_BIN_DIR)
        else:
            os.remove(__B2J_BIN_DIR)


# convert tung board to json
def board_to_json(boardPath, jsonPath):
    executablePath = os.path.join(__B2J_BIN_DIR, 'BoardToJson.exe')
    command = [executablePath, boardPath, '-i', '-o', jsonPath]
    subprocess.check_call(
        command,
        shell = False,
        stdout = subprocess.DEVNULL,
        stderr = subprocess.DEVNULL)


# convert json to tung board
def json_to_board(jsonPath, boardPath):
    executablePath = os.path.join(__B2J_BIN_DIR, 'BoardToJson.exe')
    command = [executablePath, jsonPath, '-i', '-o', boardPath]
    subprocess.check_call(
        command, shell = False,
        stdout = subprocess.DEVNULL,
        stderr = subprocess.DEVNULL)
