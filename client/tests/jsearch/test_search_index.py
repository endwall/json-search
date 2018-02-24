from unittest import TestCase

from mock import MagicMock, call, patch
from nose.tools import raises

from client.jsearch.search_index import BaseIndex, UntokenizedSearchIndex

class TestBaseIndex(TestCase):
    """Test the BaseIndex module."""

    def setUp(self):
        """Do setup."""

    @patch('client.jsearch.search_index.BaseIndex._loads')
    def test_init_without_dumps(self, mock_loads):
        base_index = BaseIndex()
        self.assertTrue(mock_loads.called)
        self.assertEqual(base_index.index_meta, {})
        self.assertEqual(base_index.indices, {})
        self.assertEqual(base_index.document_dict, {})

    @patch('client.jsearch.search_index.pickle.load')
    @patch('client.jsearch.search_index.json.load')
    @patch('client.jsearch.search_index.open')
    @patch('client.jsearch.search_index.os.path.isfile')
    def test_loads(self, mock_isfile, mock_open, mock_json_load, mock_pickle_load):
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
        mock_pickle_load.side_effect = [
            {
                'user': {
                    '123': {'email': 'test@email'}
                }
            },
            {
                'email': {
                    'test@email' : '123'
                }
            }
        ]
        base_index = BaseIndex()
        self.assertTrue(mock_isfile.called)
        self.assertEqual(mock_isfile.call_args, call('./data/meta.json'))
        self.assertEqual(mock_open.call_count, 3)
        self.assertEqual(mock_pickle_load.call_count, 2)
        self.assertEqual(base_index.index_meta, mock_json_load.return_value)
        self.assertEqual(base_index.indices.keys()[0], 'user')
        self.assertEqual(base_index.indices['user'], {'email': {'test@email' : '123'}})