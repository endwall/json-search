#!/usr/bin/env python
# encoding=utf8
"""
A CLI utility to do json search.

Please see project README for more information.

"""
from __future__ import print_function

import argparse
import os
import sys

# The search subcommand
def add_search(subparsers):
    """Add subcommand search into parser."""
    parser = subparsers.add_parser(
        'search',
        help='search by string value in an object namespace',
        description='currently only exact match is supported (case insensitive)',
    )
    parser.add_argument(
        '-v', '--value', type=str,
        help='the string to be searched',
    )
    parser.add_argument(
        '-o', '--object', type=str,
        help='objects to be searched, can be user, organization and ticket'
    )
    parser.set_defaults(func=handle_search)

def handle_search(args):
    """Search string in a given object."""

# The list subcommand
def add_list(subparsers):
    """Add subcommand list into parser."""
    parser = subparsers.add_parser(
        'list',
        help='list structure of a given object',
        description='list object structure',
    )
    parser.add_argument(
        '-t', '--type', type=str,
        help='type to list, such as object, keys, etc',
    )
    parser.add_argument(
        '-o', '--object', type=str,
        default='all',
        help='object(s) to be listed'
    )
    parser.set_defaults(func=handle_list)

def handle_list(args):
    """list structure of a given object."""

def parse_args(parser, arglist=None):
    """Add more logic after parser.parse_args."""
    args = parser.parse_args(arglist)
    return args

# parser related functions
def create_parser():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        usage='%(prog)s [subcommand]', description=__doc__,
    )
    subparsers = parser.add_subparsers(
        title='subcommands',
    )

    add_list(subparsers)
    add_search(subparsers)
    return parser

def main():
    """Parse command args and run the handler function for the subcommand."""
    args = parse_args(create_parser())
    args.func(args)


if __name__ == '__main__':
    main()