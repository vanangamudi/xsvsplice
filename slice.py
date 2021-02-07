#!/usr/bin/env python3

import os
import csv
import sys
import argparse

import logging
logging.basicConfig()

log = logging.getLogger('main')
log.setLevel(logging.INFO)

from pprint import pprint, pformat

from formats import FORMATS

parser = argparse.ArgumentParser()

parser.add_argument("-v",
                    "--verbose",
                    help="increase output verbosity",
                    action="store_true",
)

parser.add_argument("-p",
                    "--prefix",
                    help="prefix for filepath",
                    default='',
)

parser.add_argument("-D",
                    "--debug",
                    help="set debugging mode on",
                    action='store_true',
)

parser.add_argument("-H",
                    "--header",
                    help="use column headers as part of output filenames",
                    action='store_true',
)


parser.add_argument("input_",
                    help="input file",
                    nargs='+',
)

args = parser.parse_args(sys.argv)
print(parser.prog, args)

if args.debug:
    log.setLevel(logging.DEBUG)


args.input_ = args.input_[1]

if not args.prefix:
    args.prefix = os.path.basename(
        os.path.splitext(args.input_)[0]
    )

ext = os.path.splitext(args.input_)[-1][1:]

with open(args.input_) as input_file:
    lines = input_file.read().replace('\r', '').split('\n')
    log.debug(pformat(lines[-10:]))

    lines = [line for line in lines if len(line.strip())]
    log.debug(pformat(lines[-10:]))

    lines = [ line.split(FORMATS[ext]) for line in lines ]
    log.debug(pformat(lines[-10:]))

    column_count = [len(line) for line in lines]
    fields_count = sum(column_count)
    lines_count = len(lines)
    log.debug( "lengths of lines " + pformat( list(
        (i, count) for i, count in enumerate(column_count) if count != column_count[0]
    )))

    assert fields_count % lines_count == 0, \
        '{} % {} = {}'.format(fields_count, lines_count, fields_count % lines_count)

    content = list(zip(*lines))

    print('total number of columns: {}'.format(len(content)))

    if args.header:
        output_filepaths = ['{}-col{:04d}-{}.{}'.format(args.prefix, i, c[0], ext)
                            for i, c in enumerate(content) ]

    else:
        output_filepaths = ['{}-col{:04d}.{}'.format(args.prefix, i, ext)
                            for i, c in enumerate(content) ]

    for filepath, c in zip(output_filepaths, content):
        with open(filepath, 'w') as output_file:
            log.debug(pformat(c))
            output_file.write('\n'.join(c))
