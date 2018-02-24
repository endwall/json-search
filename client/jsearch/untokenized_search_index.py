#
# Indexing Json files
#
import hashlib
import json
import os
from blist import sortedset
from client.jsearch.base_search_index import BaseIndex

class UntokenizedSearchIndex(BaseIndex):
	def index_document(self, table_name, index_name, token, document, uid=None):
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
		self.update_document(table_name=table_name, uid = _uid, document = document)

	def search(self, table_name, index_name, token):
		doc_uid_list = []
		result = []
		if token in self.indices[table_name][index_name]:
			doc_uid_list = self.indices[table_name][index_name][token]
		for doc_uid in doc_uid_list:
			result.append(self.document_dict[table_name][doc_uid])
		return result
	
