#!/usr/bin/env python3
import os
import csv
import sys
import argparse

import logging

from formats import FORMATS

parser = argparse.ArgumentParser()

parser.add_argument("-v",
                    "--verbose",
                    help="increase output verbosity",
                    action="store_true"
)

parser.add_argument("-o",
                    "--output",
                    help="destination filepath",
)


parser.add_argument("files",
                    help="list of files",
                    nargs='+',
)


args = parser.parse_args(sys.argv)
print(parser.prog, args)


files_content = [open(filepath).read().split('\n') for filepath in args.files[1:]]

files_content = zip(*files_content)
ext = os.path.splitext(args.output)[-1][1:]
with open(args.output, 'w') as f:
    f.write(
        '\n'.join([
            FORMATS[ext].join(row) for row in files_content
        ])
    )
