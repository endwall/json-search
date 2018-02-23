#
# Indexing Json files
#

import hashlib
import json
import pickle
import os

class BaseIndex(object):
	META_FILE = 'meta.json'
	def __init__(self, dest='./data/'):
		self.data_path = dest
		self.index_meta = {}
		self.indices = {}
		self.document_dict = {}
		if os.path.lexists(dest + self.META_FILE):
			self.index_meta = json.loads(open(dest + self.META_FILE).read())
			self._loads()

	def add_table(self, table_name):
		self.indices[table_name] = {}

	def add_index(self, table_name, index_name):
		if table_name not in self.indices:
			self.add_table(table_name)
		if index_name not in self.indices[table_name]:
			self.indices[table_name][index_name] = {}

	def update_index_table_meta(self):
		for table in self.indices:
			self.index_meta[table] = self.indices[table].keys()

	def list(self, table_name=None):
		if table_name is None:
			return self.indices.keys()
		else:
			return self.indices[table_name]

	def index_document(self, table_name, index_name, token, document, uid=None):
		pass

	def search(self, table_name, index_name, tokens):
		pass

	def _loads(self):
		with open(self.index_meta['doc']) as doc_file:
			self.document_dict = pickle.load(doc_file)
		for table in self.index_meta['tables']:
			with open(self.index_meta['tables'][table]) as table_file:
			    self.indices[table] = pickle.load(table_file)

	def dumps(self):
		meta_file = self.data_path + self.META_FILE
		self.index_meta['tables'] = {}
		for table in self.indices:
			print("dump index: " + table)
			output_file = open(self.data_path + table + '.idx', 'wb')
			pickle.dump(self.indices[table], output_file)
			output_file.close()
			self.index_meta['tables'][table] = self.data_path + table + '.idx'
		output_file = open(self.data_path + table + '.dat', 'wb')
		pickle.dump(self.document_dict, output_file)
		output_file.close()
		self.index_meta['doc'] = self.data_path + table + '.dat'
		print(self.index_meta)
		with open(meta_file, 'wb') as outfile:
			json.dump(self.index_meta, outfile)		

class UntokenizedSearchIndex(BaseIndex):
	def index_document(self, table_name, index_name, token, document, uid=None):
		if table_name not in self.indices:
			self.indices[table_name] = {}
		current_table = self.indices[table_name]

		if index_name not in current_table:
			current_table[index_name] = {}
		current_index = current_table[index_name]

		if token not in current_index:
			current_index[token] = []
		_uid = uid

		if _uid is None:
			_uid = hashlib.md5(json.dumps(document, sort_keys=True)).hexdigest()
		current_index[token].append(_uid)
		self.document_dict[_uid] = document

	def search(self, table_name, index_name, token):
		doc_uid_list = []
		result = []
		if token in self.indices[table_name][index_name]:
			doc_uid_list = self.indices[table_name][index_name][token]
		for doc_uid in doc_uid_list:
			result.append(self.document_dict[doc_uid])
		return result
	
