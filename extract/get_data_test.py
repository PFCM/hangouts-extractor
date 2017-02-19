"""tests for get_data.py"""
import unittest
import tempfile
import hashlib
import os

from nose2.tools import params

import extract.get_data as get_data


def _gen_fake_data(path):
    """make some false data, save it into path"""
    pass


def _get_hash(path):
    """hash a file"""
    hasher = hashlib.sha1()
    with open(path, 'rb') as fp:
        # only expecting small files so just hash the lot all at once
        hasher.update(fp.read())
    return hasher.hexdigest()


class TestGetData(unittest.TestCase):

    _test_filename = None
    _test_file_hash = None

    @classmethod
    def setUpClass(cls):
        # write a little skeleton file that can be used for testing
        # creating and deleting it once per test is silly, although we will
        # make sure to add a hook to check it hasn't been changed
        if not cls._test_filename:
            _, cls._test_filename = tempfile.mkstemp(text=True)
            _gen_fake_data(cls._test_filename)
            cls._test_file_hash = _get_hash(cls.test_filename)

    @classmethod
    def tearDownClass(cls):
        # delete the test file
        os.remove(cls._test_filename)
        cls._test_filename = None

    def test_get_conversations(self):
        pass
