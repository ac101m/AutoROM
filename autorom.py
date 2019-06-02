#!/usr/bin/env python3


# standard
import os
import argparse
import json
import tkinter as tk


# this project
import autorom_b2j as b2j


# Set up command line argument parser
def build_option_parser():
    parser = argparse.ArgumentParser(description = 'Generate big ROMs for tung')

    parser.add_argument(
        '-u', '--updateb2j', action = 'store_true',
        help = 'Re-download currently installed BTJ (board to json) instance')

    return parser


# let's go
def main():
    args = build_option_parser().parse_args()
    root = tk.Tk()
    root.withdraw()

    # User initiated update of b2j
    if args.updateb2j:
        print("Removing B2J binaries...")
        b2j.uninstall()

    # Check that boardtojson (b2j) is present, if not, get it
    if not b2j.installed():
        print("B2J binaries not present, installing...")
        b2j.install()

    # Try to convert a board [TEMP]
    boardDir = os.path.dirname(__file__) + '/boards/'
    tungBoard = boardDir + 'rom-matrix-8kB.tungboard'
    jsonBoard = boardDir + 'rom-matrix-8kB.json'
    b2j.board_to_json(tungBoard, jsonBoard)


# make this importable
if __name__ == '__main__':
    main()
