from unittest import TestCase

from mock import MagicMock, call, patch
from nose.tools import raises
import hashlib
import json
from blist import sortedset

from client.jsearch.untokenized_search_index import UntokenizedSearchIndex

class TestUntokenizedSearchIndex(TestCase):

    @patch('client.jsearch.untokenized_search_index.UntokenizedSearchIndex._loads')
    def setUp(self, mock_index_loads):
        """Do setup."""
        self.search_index = UntokenizedSearchIndex()
        self.search_index.indices = {
            'user': {
                'email': {
                    'abc@g.com': sortedset(['35cc47af8dcdbc9cf700dbd7dfe6a5a1'])
                }
            }
        }
        self.search_index.document_dict = {
            'user': {
                '35cc47af8dcdbc9cf700dbd7dfe6a5a1': {'email': 'abc@g.com'}
            }
        }

    def test_index_document(self):
        doc = {
            'email': 'aaa@h.com'
        }
        uid = hashlib.md5(json.dumps(doc, sort_keys=True)).hexdigest()
        self.search_index.index_document(table_name='user', index_name='email', token='aaa@h.com', document=doc)
        self.assertEqual(self.search_index.indices, {
            'user': {'email': {
                'abc@g.com': sortedset(['35cc47af8dcdbc9cf700dbd7dfe6a5a1']),
                'aaa@h.com': sortedset([uid])
            }}
        })

    def test_index_duplicated_document(self):
        doc = {
            'email': 'abc@g.com'
        }
        uid = hashlib.md5(json.dumps(doc, sort_keys=True)).hexdigest()
        self.search_index.index_document(table_name='user', index_name='email', token='abc@g.com', document=doc)
        self.assertEqual(self.search_index.indices, {
            'user': {'email': {
                'abc@g.com': sortedset(['35cc47af8dcdbc9cf700dbd7dfe6a5a1'])
            }}
        })        

    def test_search(self):
        query = 'abc@g.com'
        result = self.search_index.search(table_name='user', index_name='email', token=query)
        self.assertEqual(result, [{'email': 'abc@g.com'}])

    def test_search_empty_without_result(self):
        query = ''
        result = self.search_index.search(table_name='user', index_name='email', token=query)
        self.assertEqual(result, [])

    def test_search_empty_with_result(self):
        query = ''
        doc = {'email': ''}
        self.search_index.index_document(table_name='user', index_name='email', token='', document=doc)
        self.assertEqual(self.search_index.indices, {
            'user': {'email': {
                '': sortedset(['ee3161ffa6dad871caedeed6e2298654']),
                'abc@g.com': sortedset(['35cc47af8dcdbc9cf700dbd7dfe6a5a1'])
            }}
        })
        result = self.search_index.search(table_name='user', index_name='email', token='')
        self.assertEqual(result, [{'email': ''}])
