#!/usr/bin/env python3

# Copyright (c) 2022, Pelion Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Script to convert DER files into C arrays."""

import argparse
import binascii
import pathlib
import sys


def _str_to_resolved_path(path_str):
    """
    Convert a string to a resolved Path object.

    Args:
    * path_str (str): string to convert to a Path object.

    """
    return pathlib.Path(path_str).resolve(strict=False)


def _parse_args():
    # Parse command line
    parser = argparse.ArgumentParser(description="Convert DER into c file")
    parser.add_argument(
        "--public",
        type=_str_to_resolved_path,
        help="public key",
    )
    parser.add_argument(
        "--private",
        type=_str_to_resolved_path,
        help="private key",
    )
    parser.add_argument(
        "--output",
        type=_str_to_resolved_path,
        help="Output C file",
        required=True,
    )
    args, unknown = parser.parse_known_args()

    if len(unknown) > 0:
        warning("unsupported arguments: {}".format(unknown))

    return args


def _process_data(infile, outfile, name):
    # Process data
    outfile.write("const unsigned char {}[] =\n".format(name))
    outfile.write("{\n")
    with open(infile, "rb") as dataFile:
        while True:
            hexdata = dataFile.read(16).hex()
            if len(hexdata) == 0:
                break
            hexlist = map("".join, zip(hexdata[::2], hexdata[1::2]))
            outfile.write("    ")
            for thing in hexlist:
                outfile.write("0x{}, ".format(thing))
            outfile.write("\n")
    outfile.write("};\n")

    outfile.write("const unsigned int {0}_SIZE = sizeof({0});\n".format(name))


def main():
    """Perform the main execution."""
    args = _parse_args()

    with open(args.output, "w") as output_data:
        output_data.write("#ifndef __DEV_CREDENTIALS_H__\n")
        output_data.write("#define __DEV_CREDENTIALS_H__\n")
        if args.private is not None:
            _process_data(args.private, output_data, "DEV_BOOTSTRAP_DEVICE_PRIVATE_KEY")
        if args.public is not None:
            _process_data(args.public, output_data, "DEV_BOOTSTRAP_DEVICE_CERTIFICATE")
        output_data.write("#endif //__DEV_CREDENTIALS_H__\n")


if __name__ == "__main__":
    sys.exit(main())
