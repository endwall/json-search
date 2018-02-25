"""Simple implentaton of json index.

All indexed tokens are lowercase string.
Token can be hashed as well instead of the actually string.

"""

import hashlib
import json

from blist import sortedset

from base_search_index import BaseIndex


class UntokenizedSearchIndex(BaseIndex):
    """Simplest impletation for a search index."""

    def index_document(self, table_name, index_name, token, document, uid=None):
        """Indexing a single document."""
        if table_name not in self.indices:
            self.indices[table_name] = {}
        current_table = self.indices[table_name]

        if index_name not in current_table:
            current_table[index_name] = {}
        current_index = current_table[index_name]

        if token not in current_index:
            current_index[token] = sortedset([])
        _uid = uid

        if _uid is None:
            _uid = hashlib.md5(json.dumps(document, sort_keys=True)).hexdigest()
        current_index[token].add(_uid)
        self.update_document(table_name=table_name, uid=_uid, document=document)

    def search(self, table_name, index_name, token):
        """Search by exact match a token against an index."""
        doc_uid_list = []
        result = []
        if token in self.indices[table_name][index_name]:
            doc_uid_list = self.indices[table_name][index_name][token]
        for doc_uid in doc_uid_list:
            result.append(self.document_dict[table_name][doc_uid])
        return result
