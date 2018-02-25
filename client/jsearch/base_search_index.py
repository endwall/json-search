"""Base Index class.

To create inverted index, there are many steps.
Could add more functions such as tokenization, Stemming, etc
"""

import json
import os
import pickle


class BaseIndex(object):
    """Base class for inverted search index."""

    META_FILE = 'meta.json'

    def __init__(self, dest='./data/'):
        """Initialize internal data structures and loads existing indices."""
        self.data_path = dest
        self.index_meta = {}
        self.indices = {}
        self.document_dict = {}
        self._loads()

    def add_table(self, table_name):
        """Add an empty index table."""
        self.indices[table_name] = {}

    def add_index(self, table_name, index_name):
        """Add an empty index."""
        if table_name not in self.indices:
            self.add_table(table_name)
        if index_name not in self.indices[table_name]:
            self.indices[table_name][index_name] = {}

    def update_index_table_meta(self):
        """Update index table meta data."""
        for table in self.indices:
            self.index_meta[table] = self.indices[table].keys()

    def list(self, table_name=None):
        """List Index Table and search keys."""
        if table_name is None:
            return self.indices.keys()
        else:
            return self.indices[table_name].keys()

    def index_document(self, table_name, index_name, token, document, uid=None):
        """Indexing a ducument."""
        pass

    def search(self, table_name, index_name, tokens):
        """Search by token."""
        pass

    def _loads(self):
        if os.path.isfile(self.data_path + self.META_FILE):
            with open(self.data_path + self.META_FILE, 'r') as meta_file:
                self.index_meta = json.load(meta_file)
            with open(self.index_meta['doc']) as doc_file:
                self.document_dict = pickle.load(doc_file)
            for table in self.index_meta['tables']:
                with open(self.index_meta['tables'][table]) as table_file:
                    self.indices[table] = pickle.load(table_file)

    def dumps(self):
        """Entry of dumping internal data."""
        self.index_meta = {}
        try:
            if not os.path.exists(self.data_path):
                os.makedirs(self.data_path)
            self._dump_indices()
            self._dump_docs()
            self._dump_indices_meta()
        except OSError:
            print('Error: Fail to create directory ' + self.data_path)
            raise

    def _dump_indices(self):
        """Dump indices."""
        self.index_meta['tables'] = {}
        for table in self.indices:
            with open(self.data_path + table + '.idx', 'wb') as output_file:
                pickle.dump(self.indices[table], output_file)
            self.index_meta['tables'][table] = self.data_path + table + '.idx'

    def _dump_docs(self):
        """Dump all documents map."""
        self.index_meta['doc'] = {}
        with open(self.data_path + 'doc.dat', 'wb') as output_file:
            pickle.dump(self.document_dict, output_file)
        self.index_meta['doc'] = self.data_path + 'doc.dat'

    def _dump_indices_meta(self):
        """Dump Indices meta data."""
        meta_file = self.data_path + self.META_FILE
        with open(meta_file, 'wb') as outfile:
            json.dump(self.index_meta, outfile)

    def update_document(self, table_name, uid, document):
        """Update document dict."""
        if table_name not in self.document_dict:
            self.document_dict[table_name] = {}
        self.document_dict[table_name][uid] = document
