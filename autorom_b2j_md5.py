#!/usr/bin/env python3

# MakeROM downloads BoardToJson binaries AND runs them autonomously.
# Naturally, this is a potentially dodgy situation.
# So, if the fetched archive does not match any of the MD5 sums in this file
# then the user will be prompted


# Standard
import hashlib


# Vector of accepted MD5 checksums for B2J binaries
__B2J_MD5 = ['e65eebceacdce2a976c6a8b4e6242aa3']


# Generate md5 checksum for arbitrary file
def hex_digest(path):
    md5 = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)
    return md5.hexdigest()


# Check if a file matches any of the above checksums
def check(path):
    fileMD5 = hex_digest(path)
    for validMD5 in __B2J_MD5:
        if validMD5 == fileMD5:
            return False
    return True
