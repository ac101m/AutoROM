#!/usr/bin/env python3


# standard
import os
import sys
import argparse
import json
import tkinter as tk


# this project
import autorom_b2j as b2j
from autorom_image import rom_image


# Set up command line argument parser
def build_option_parser():
    parser = argparse.ArgumentParser(description = 'Generate big ROMs for tung')

    parser.add_argument(
        '-u', '--updateb2j', action = 'store_true',
        help = 'Re-install BTJ (board to json) binaries')

    parser.add_argument(
        '-i', '--input', type = str,
        help = 'Input file. Extension determines parsing behaviour, this is ' +
               'a mandatory parameter')

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

    # Get input file as ROM image
    if args.input == None:
        print("ERROR, no input file specified, please specify an input file")
        sys.exit()

    # Decode the input file
    image = rom_image(args.input, 512)
    image.print_all()


# make this importable
if __name__ == '__main__':
    main()
