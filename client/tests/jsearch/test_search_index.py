from unittest import TestCase

from mock import MagicMock, call, patch
from nose.tools import raises

from client.jsearch.search_index import BaseIndex, UntokenizedSearchIndex

class TestBaseIndex(TestCase):
    """Test the BaseIndex module."""

    def setUp(self):
        """Do setup."""

    @patch('client.jsearch.search_index.os.path.lexists')
    def test_init(self, mock_lexists):
    	mock_lexists.return_value = False
    	base_index = BaseIndex()
    	self.assertTrue(mock_lexists.called)
    	self.assertEqual(base_index.index_meta, {})
