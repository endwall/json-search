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
import json
import types

from jsearch.search_index import UntokenizedSearchIndex

# The indexing subcommand
def add_indexing(subparsers):
    """Add subcommand indexing into parser."""
    parser = subparsers.add_parser(
        'index',
        help='indexing json objects',
        description='currently only exact match is supported (case insensitive)',
    )
    parser.add_argument(
        '-t', '--table-name', type=str,
        help='indices table name',
    )
    parser.add_argument(
        '-f', '--json-file', type=str,
        help='json files to be indexed'
    )
    parser.set_defaults(func=handle_indexing)

def handle_indexing(args):
    """indexing json files"""
    search_index = UntokenizedSearchIndex()
    data = json.loads(open(args.json_file).read())
    for doc in data:
        for key, value in doc.iteritems():
            if type(value) is list:
                for subval in value:
                    search_index.index_document(table_name=args.table_name, 
                        index_name=key,
                        token=subval.lower(),
                        document=doc)
            elif type(value) is unicode:
                search_index.index_document(table_name=args.table_name, 
                    index_name=key,
                    token=value.encode('utf-8').lower(),
                    document=doc)
            elif type(value) is not str:
                search_index.index_document(table_name=args.table_name, 
                    index_name=key,
                    token=str(value).lower(),
                    document=doc)                    
            else:
                search_index.index_document(table_name=args.table_name, 
                    index_name=key,
                    token=value.lower(),
                    document=doc)                
    search_index.dumps()

# The search subcommand
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
    parser.set_defaults(func=handle_search)

def handle_search(args):
    """Search string in a given object."""
    search_index = UntokenizedSearchIndex()
    result = search_index.search(table_name=args.table_name, index_name=args.field_name, token=args.query.lower())
    print(json.dumps(result, indent=4))

# The list subcommand
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
    """list structure of a given object."""
    search_index = UntokenizedSearchIndex()
    print(json.dumps(search_index.list()))

def parse_args(parser, arglist=None):
    """Add more logic after parser.parse_args."""
    args = parser.parse_args(arglist)
    return args

# parser related functions
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
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

def main():
    """Parse command args and run the handler function for the subcommand."""
    args = parse_args(create_parser())
    args.func(args)


if __name__ == '__main__':
    main()