#!/usr/bin/env python
# encoding=utf8
"""
A CLI utility to do json search.

Please see project README for more information.

"""
from __future__ import print_function

import argparse
import json
import sys

from indexing_helper import IndexingHelper
from output_helper import OutputHelper
from untokenized_search_index import UntokenizedSearchIndex


def add_indexing(subparsers):
    """Add subcommand indexing into parser."""
    parser = subparsers.add_parser(
        'index',
        help='indexing json objects',
        description='currently only exact match is supported (case insensitive)',
    )
    parser.add_argument(
        '-t', '--table-name', type=str,
        required=True,
        help='indices table name',
    )
    parser.add_argument(
        '-f', '--json-file', type=str,
        required=True,
        help='json files to be indexed'
    )
    parser.set_defaults(func=handle_indexing)


def handle_indexing(args):
    """Indexing json files."""
    helper = IndexingHelper()

    helper.handle_indexing(table_name=args.table_name, doc_file=args.json_file)


def add_search(subparsers):
    """Add subcommand search into parser."""
    parser = subparsers.add_parser(
        'search',
        help='search by string value in an object namespace',
        description='currently only exact match is supported (case insensitive)',
    )
    parser.add_argument(
        '-t', '--table-name', type=str,
        required=True,
        help='indices table name',
    )
    parser.add_argument(
        '-f', '--field-name', type=str,
        required=True,
        help='indices field name',
    )
    parser.add_argument(
        '-q', '--query', type=str, default='',
        help='the string to be searched',
    )
    parser.add_argument(
        '-o', '--output-type', type=str, default='table',
        help='output format',
    )
    parser.set_defaults(func=handle_search)


def handle_search(args):
    """Search string in a given object."""
    search_index = UntokenizedSearchIndex()
    result = search_index.search(
        table_name=args.table_name,
        index_name=args.field_name,
        token=args.query.lower())
    output_helper = OutputHelper()
    output_helper.output_json(input_json=result, format=args.output_type)


def add_list(subparsers):
    """Add subcommand list into parser."""
    parser = subparsers.add_parser(
        'list',
        help='list structure of a given object',
        description='list object structure',
    )
    parser.add_argument(
        '-t', '--table-name', type=str,
        help='object to list, such as object, keys, etc',
    )
    parser.set_defaults(func=handle_list)


def handle_list(args):
    """List structure of a given object."""
    search_index = UntokenizedSearchIndex()
    print(json.dumps(search_index.list(table_name=args.table_name)))


def parse_args(parser, arglist=None):
    """Add more logic after parser.parse_args."""
    args = parser.parse_args(arglist)
    return args


def create_parser():
    """Parse command line arguments."""
    parser = CustomParser(
        usage='%(prog)s [subcommand]', description=__doc__,
    )
    subparsers = parser.add_subparsers(
        title='subcommands',
    )

    add_list(subparsers)
    add_search(subparsers)
    add_indexing(subparsers)
    return parser


class CustomParser(argparse.ArgumentParser):
    """Customized parser to allow printing help when args are wrong."""

    def error(self, message):
        """Override ArgumentParser.error."""
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def main():
    """Parse command args and run the handler function for the subcommand."""
    args = parse_args(create_parser())
    args.func(args)


if __name__ == '__main__':
    main()
