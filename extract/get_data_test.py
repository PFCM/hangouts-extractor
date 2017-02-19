"""tests for get_data.py"""
import unittest
import tempfile
import hashlib
import random
import string
import os

from nose2.tools import params

import extract.get_data as get_data


def _fake_chats():
    pass

def _fake_person():
    person_id = _fake_id()
    return {
        'id': {
            'gaia_id': person_id,
            'chat_id': person_id
        },
        'fallback_name': ''.join(random.choices(string.ascii_lowercase, k=10)),
        'invitation_status': 'ACCEPTED_INVITATION',
        'participant_type': 'GAIA',
        'new_invitation_status': 'ACCEPTED_INVITATION'
    }


def _fake_people():
    if random.random() > 0.7:
        num_people = random.randint(2, 4)
    else:
        num_people = 2

    return [_fake_person() for _ in range(num_people)]


def _fake_id():
    """uses random.randint, assumes you've appropriately seeded"""
    return hex(random.randint())


def _fake_conv(seed=123):
    """make a random conversation, in a way deterministic on `seed`"""
    random.seed(seed)
    conversation_id = _fake_id()
    participants = _fake_people()
    data = {
        'conversation_id': {
            'id': conversation_id
        },
        'response_header': {
            'status': 'OK',
            'debug_url': '',
            'request_trace_id': _fake_id(),
            'current_server_time': str(random.randint()),
            'build_label': '',
            'changelist_number': str(random.randint())
        },
        'conversation_state': {
            'conversation_id': {
                'id': conversation_id
            },
            'conversation': {
                'id': {
                    'id': conversation_id
                },
                'type': 'STICKY_ONE_TO_ONE',
                'self_conversation_state': {
                    'self_read_state': {
                        'participant_id': {
                            'gaia_id': _fake_id(),
                            'chat_id': _fake_id()
                        },
                        'latest_read_timestamp': _fake_id(),
                    },
                    'status': 'ACTIVE',
                    'notification_level': 'RING',
                    'view': ['INBOX_VIEW'],
                    'inviter_id': {
                        'gaia_id': _fake_id(),
                        'chat_id': _fake_id()
                    },
                    'invite_timestamp': str(random.randint()),
                    'sort_timestamp': str(random.randint()),
                    'active_timestamp': str(random.randint()),
                    'delivery_medium_option': [{
                        'delivery_medium': {
                            'medium_type': 'BABEL_MEDIUM'
                        },
                        'current_default': True,
                    }],
                    'is_guest': False
                },
                'participant_data': participants,
                'event': _fake_chats(participants)
            }
        }
    }


def _gen_fake_data(path):
    """make some false data, save it into path"""
    data = {'conversation_state': [_fake_conv(i) for i in range(10)]}
    return data


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
    def test_hash(cls, filename):
        # check the file hasn't been changed
        cls.assertEqual(_get_hash(filename), cls._test_file_hash)

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
