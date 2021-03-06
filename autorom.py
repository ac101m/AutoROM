#!/usr/bin/env python3


# standard
import os
import sys
import argparse
import json
import tkinter as tk


# this project
import rom.registry as RomRegistry
import util.env as env
import util.b2j as b2j
from rom.encode import TungRomEncoder
from util.image import RomImage


# Set up command line argument parser
def build_option_parser():
    parser = argparse.ArgumentParser(
        description = 'AutoROM is a utility for importing files into TUNG ' +
                      'as read-only memory.')

    # Update board to json from github (optional, exclusive)
    parser.add_argument(
        '-c', '--clean', action = 'store_true',
        help = "Clean all local files.")

    # Select input file (mandatory)
    parser.add_argument(
        '-i', '--input', type = str,
        help = 'Input file. Extension determines parsing behaviour, this is ' +
               'a mandatory parameter.')

    # List ROM board info (optional, exclusive)
    parser.add_argument(
        '-l', '--listrom', action = 'store_true',
        help = 'List information for all available ROM boards.')

    # Select ROM board to load to (mandatory)
    parser.add_argument(
        '-r', '--romtype', choices = RomRegistry.get_rom_ids(),
        help = 'Name of ROM board to load data into. This is mandatory ' +
               'parameter.')

    # Select output file (optional)
    parser.add_argument(
        '-o', '--output', type = str,
        help = 'Output file. By default, the filename will be a combination ' +
               'of the selected ROM board and the name of the file from ' +
               'which it was initialised.')

    return parser


# let's go
def main():
    args = build_option_parser().parse_args()
    root = tk.Tk()
    root.withdraw()

    # User initiated update of b2j
    if args.clean:
        print("Cleaning local files...")
        b2j.uninstall()
        RomRegistry.clean()
        env.clean()
        return

    # User requested board info
    if args.listrom:
        RomRegistry.print_all()
        return

    # Check that boardtojson (b2j) is present, if not, get it
    if not b2j.installed():
        print("B2J binaries not present, installing...")
        b2j.install()

    # Get input file as ROM image
    if args.input == None:
        print("ERROR: No input file specified. Please specify an input file.")
        sys.exit()

    # Get ROM type
    if args.romtype == None:
        print('ERROR: No ROM type specified. Please specify a ROM type.')
        sys.exit()

    # Decode the input file
    try:
        image = RomImage(RomRegistry.get_capacity(args.romtype), args.input)
    except FileNotFoundError:
        print("ERROR: Input file '" + args.input + "' not found. " +
              "Nothing to be done.")
        sys.exit()

    # Compute path for output file
    inFile = os.path.basename(args.input)
    outputFile = args.romtype + '(' + inFile + ').tungboard'
    if args.output != None:
        if os.path.isdir(args.output):
            outputFile = os.path.join(args.output, outputFile)
        else:
            outputFile = args.output

    # Output the ROM
    encoder = TungRomEncoder(args.romtype)
    encoder.encode(outputFile, image)


# make this importable
if __name__ == '__main__':
    main()
