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
		if os.path.isfile(self.data_path + self.META_FILE):
			with open(self.data_path + self.META_FILE, 'r') as meta_file:
				self.index_meta = json.load(meta_file)
			with open(self.index_meta['doc']) as doc_file:
				self.document_dict = pickle.load(doc_file)
			for table in self.index_meta['tables']:
				with open(self.index_meta['tables'][table]) as table_file:
				    self.indices[table] = pickle.load(table_file)

	def dumps(self):
		self.index_meta = {}
		self._dump_indices()
		self._dump_docs()
		self._dump_indices_meta()

	def _dump_indices(self):
		self.index_meta['tables'] = {}
		for table in self.indices:
			print("dump index: " + table)
			with open(self.data_path + table + '.idx', 'wb') as output_file:
				pickle.dump(self.indices[table], output_file)
			self.index_meta['tables'][table] = self.data_path + table + '.idx'

	def _dump_docs(self):
		self.index_meta['doc'] = {}
		with open(self.data_path + 'doc.dat', 'wb') as output_file:
			pickle.dump(self.document_dict, output_file)
		self.index_meta['doc'] = self.data_path + 'doc.dat'

	def _dump_indices_meta(self):
		meta_file = self.data_path + self.META_FILE
		with open(meta_file, 'wb') as outfile:
			json.dump(self.index_meta, outfile)		

	def update_document(self, table_name, uid, document):
		if table_name not in self.document_dict:
			self.document_dict[table_name] = {}
		self.document_dict[table_name][uid] = document

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
		self.update_document(table_name=table_name, uid = _uid, document = document)

	def search(self, table_name, index_name, token):
		doc_uid_list = []
		result = []
		if token in self.indices[table_name][index_name]:
			doc_uid_list = self.indices[table_name][index_name][token]
		for doc_uid in doc_uid_list:
			result.append(self.document_dict[table_name][doc_uid])
		return result
	
