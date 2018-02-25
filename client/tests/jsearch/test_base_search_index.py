"""Test Case for base search index class."""

from unittest import TestCase

from mock import MagicMock, call, patch

from jsearch.base_search_index import BaseIndex


class TestBaseIndex(TestCase):
    """Test the BaseIndex module."""

    def setUp(self):
        """Do setup."""

    @patch('jsearch.base_search_index.BaseIndex._loads')
    def test_init_without_dumps(self, mock_loads):
        """Test init w/o any existing indices data."""
        base_index = BaseIndex()
        self.assertTrue(mock_loads.called)
        self.assertEqual(base_index.index_meta, {})
        self.assertEqual(base_index.indices, {})
        self.assertEqual(base_index.document_dict, {})

    @patch('jsearch.base_search_index.pickle.load')
    @patch('jsearch.base_search_index.json.load')
    @patch('jsearch.base_search_index.open')
    @patch('jsearch.base_search_index.os.path.isfile')
    def test_loads(self, mock_isfile, mock_open, mock_json_load, mock_pickle_load):
        """Test loading when init."""
        mock_isfile.return_value = True
        mock_open.side_effect = [
            MagicMock(spec=file),
            MagicMock(spec=file),
            MagicMock(spec=file)
        ]
        mock_json_load.return_value = {
            'doc': './data/doc.dat',
            'tables': {
                'user': './data/user.idx'
            }
        }
        pickle_loads = [
            {
                'user': {
                    '123': {'email': 'test@email'}
                }
            },
            {
                'email': {
                    'test@email': '123'
                }
            }
        ]
        mock_pickle_load.side_effect = pickle_loads
        base_index = BaseIndex()
        self.assertTrue(mock_isfile.called)
        self.assertEqual(mock_isfile.call_args, call('./data/meta.json'))
        self.assertEqual(mock_open.call_count, 3)
        self.assertEqual(mock_pickle_load.call_count, 2)
        self.assertEqual(base_index.index_meta, mock_json_load.return_value)
        self.assertEqual(base_index.indices.keys()[0], 'user')
        self.assertEqual(base_index.indices['user'], pickle_loads[1])

    @patch('jsearch.base_search_index.pickle.dump')
    @patch('jsearch.base_search_index.open')
    @patch('jsearch.base_search_index.BaseIndex._loads')
    def test_dump_indices(self, mock_index_loads, mock_open, mock_pickle_dump):
        """Test dumping indices."""
        base_index = BaseIndex()
        base_index.indices = {
            'user': {
                '123': {'email': 'test@email'}
            }
        }
        indices_file = MagicMock(spec=file)
        mock_open.return_value(indices_file)
        base_index._dump_indices()

        self.assertTrue(mock_open.called)
        self.assertTrue(mock_pickle_dump.called)
        self.assertEqual(base_index.index_meta, {'tables': {'user': './data/user.idx'}})

    @patch('jsearch.base_search_index.pickle.dump')
    @patch('jsearch.base_search_index.open')
    @patch('jsearch.base_search_index.BaseIndex._loads')
    def test_dump_docs(self, mock_index_loads, mock_open, mock_pickle_dump):
        """Test dumping document map."""
        base_index = BaseIndex()
        base_index.indices = {
            'user': {
                '123': {'email': 'test@email'}
            }
        }
        indices_file = MagicMock(spec=file)
        mock_open.return_value(indices_file)
        base_index._dump_docs()

        self.assertTrue(mock_open.called)
        self.assertTrue(mock_pickle_dump.called)
        self.assertEqual(base_index.index_meta, {'doc': './data/doc.dat'})

    @patch('jsearch.base_search_index.json.dump')
    @patch('jsearch.base_search_index.open')
    @patch('jsearch.base_search_index.BaseIndex._loads')
    def test_dump_indices_meta(self, mock_index_loads, mock_open, mock_json_dump):
        """Test when dumping indices meta data."""
        base_index = BaseIndex()
        base_index.index_meta = {
            'doc': './data/doc.dat',
            'tables': {
                'user': './data/user.idx'
            }
        }

        indices_meta_file = MagicMock(spec=file)
        mock_open.return_value(indices_meta_file)
        base_index._dump_indices_meta()

        self.assertTrue(mock_open.called)
        self.assertTrue(mock_json_dump.called)

    @patch('jsearch.base_search_index.BaseIndex._loads')
    def test_update_document(self, mock_index_loads):
        """Test update document after indexing."""
        base_index = BaseIndex()
        base_index.document_dict = {
            'user': {
                '123': {'email': 'test@email'}
            }
        }
        new_org_doc = {
            'org_name': 'abc'
        }
        expected = {
            'user': {
                '123': {'email': 'test@email'}
            },
            'organization': {
                '222': {'org_name': 'abc'}
            }
        }
        base_index.update_document(table_name='organization', uid='222', document=new_org_doc)
        self.assertEqual(base_index.document_dict, expected)
