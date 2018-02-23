"""Unit testing for the module."""
import argparse
from unittest import TestCase

from mock import MagicMock, call, patch
from nose.tools import raises

class TestJsonSearch(TestCase):
    """Test the module."""

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

    def test_get_common_environment(self, mock_sys, mock_isfile, mock_open, mock_parse_environment):
