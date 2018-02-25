"""Indexing helper class.

Current support untokenized search index
"""

import json

from untokenized_search_index import UntokenizedSearchIndex


class IndexingHelper(object):
    """Indexing Helper class."""

    def handle_indexing(self, table_name, doc_file):
        """Process indexing subcommand."""
        search_index = UntokenizedSearchIndex()
        data = json.loads(open(doc_file).read())
        for doc in data:
            for key, value in doc.iteritems():
                if type(value) is list:
                    for subval in value:
                        search_index.index_document(
                            table_name=table_name,
                            index_name=key,
                            token=subval.lower(),
                            document=doc)
                elif type(value) is unicode:
                    search_index.index_document(
                        table_name=table_name,
                        index_name=key,
                        token=value.encode('utf-8').lower(),
                        document=doc)
                elif type(value) is not str:
                    search_index.index_document(
                        table_name=table_name,
                        index_name=key,
                        token=str(value).lower(),
                        document=doc)
                else:
                    search_index.index_document(
                        table_name=table_name,
                        index_name=key,
                        token=value.lower(),
                        document=doc)
        search_index.dumps()
