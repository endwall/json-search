"""Unit testing for the common.custom.stacker_commands module."""
import argparse
from unittest import TestCase

from mock import MagicMock, call, patch
from nose.tools import raises

class TestJsonSearch(TestCase):
    """Test the commands module."""

    def setUp(self):
        """Do setup."""
        parser = argparse.ArgumentParser()
        parser.add_argument('foo')
        self.options = parser.parse_args(['bar'])
        self.options.context = Context(
            config=Config({
                'namespace': 'test',
                'stacks': [{
                    'name': 'stack1'
                }, {
                    'name': 'stack2'
                }]
            })
        )
        self.options.region = 'ap-southeast-2'
        self.options.environment = {}

    @patch('common.custom.stacker_commands.parse_environment')
    @patch('common.custom.stacker_commands.open')
    @patch('common.custom.stacker_commands.os.path.isfile')
    @patch('common.custom.stacker_commands.sys')
    def test_get_common_environment(self, mock_sys, mock_isfile, mock_open, mock_parse_environment):
        """Get common environment values."""
        mock_sys.argv = ['foo/bar/dev.env']
        mock_isfile.return_value = True
        mock_open.return_value = MagicMock(spec=file)
        mock_parse_environment.return_value = {'foo': 'bar'}

        result = stacker_commands.get_common_environment(self.options.environment)

        self.assertTrue(mock_isfile.called)
        self.assertEqual(mock_isfile.call_args, call('foo/bar/common.env'))
        self.assertTrue(mock_open.called)
        self.assertEqual(mock_open.call_args, call('foo/bar/common.env', 'r'))
        self.assertTrue(mock_parse_environment.called)
        self.assertEqual(result, {
            'foo': 'bar',
            'env': 'dev'
        })