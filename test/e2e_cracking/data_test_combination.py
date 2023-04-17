"""Test data for test_combination.py"""
from __future__ import annotations
from .test_combination import CombinationTestInput


testdata = [
    CombinationTestInput(
        hash_type='sha1',
        hashes=[
            ('75da3d6038c28b57c8b3b34ae2f8121357bae1b9', 'footballwhatever'),
            ('6514189a7cbd9c61518d560d67690e08984e26da', ''),
            ('b4130e4e4a9cb4a7ccf58273af14b362aac9563b', ''),
            ('b471d2050dff0fd4d6baf271b8fa72b4755d846d', ''),
            ('fe1a55bca20469e048c09aa6bd4b69fe4b1c3804', '')
        ],
        left_dictionaries=['english.txt'],
        right_dictionaries=['adobe100.txt'],
        left_rule='',
        right_rule=''
    ),
    CombinationTestInput(
        hash_type='sha1',
        hashes=[
            ('75da3d6038c28b57c8b3b34ae2f8121357bae1b9', ''),
            ('6514189a7cbd9c61518d560d67690e08984e26da', 'football-whatever'),
            ('b4130e4e4a9cb4a7ccf58273af14b362aac9563b', ''),
            ('b471d2050dff0fd4d6baf271b8fa72b4755d846d', ''),
            ('fe1a55bca20469e048c09aa6bd4b69fe4b1c3804', '')
        ],
        left_dictionaries=['english.txt'],
        right_dictionaries=['adobe100.txt'],
        left_rule='$-',
        right_rule=''
    ),
    CombinationTestInput(
        hash_type='sha1',
        hashes=[
            ('75da3d6038c28b57c8b3b34ae2f8121357bae1b9', ''),
            ('6514189a7cbd9c61518d560d67690e08984e26da', ''),
            ('b4130e4e4a9cb4a7ccf58273af14b362aac9563b', ''),
            ('b471d2050dff0fd4d6baf271b8fa72b4755d846d', ''),
            ('fe1a55bca20469e048c09aa6bd4b69fe4b1c3804', 'blobspassword!')
        ],
        left_dictionaries=['english.txt'],
        right_dictionaries=['adobe100.txt'],
        left_rule='',
        right_rule='$!'
    ),
    CombinationTestInput(
        hash_type='sha1',
        hashes=[
            ('75da3d6038c28b57c8b3b34ae2f8121357bae1b9', ''),
            ('6514189a7cbd9c61518d560d67690e08984e26da', ''),
            ('b4130e4e4a9cb4a7ccf58273af14b362aac9563b', 'Matrix-SECRET!!!'),
            ('b471d2050dff0fd4d6baf271b8fa72b4755d846d', ''),
            ('fe1a55bca20469e048c09aa6bd4b69fe4b1c3804', '')
        ],
        left_dictionaries=['english.txt'],
        right_dictionaries=['darkweb2017-top1000.txt'],
        left_rule='c $-',
        right_rule='u $! $! $!'
    ),
    CombinationTestInput(
        hash_type='sha1',
        hashes=[
            ('75da3d6038c28b57c8b3b34ae2f8121357bae1b9', 'footballwhatever'),
            ('6514189a7cbd9c61518d560d67690e08984e26da', ''),
            ('b4130e4e4a9cb4a7ccf58273af14b362aac9563b', ''),
            ('b471d2050dff0fd4d6baf271b8fa72b4755d846d', ''),
            ('fe1a55bca20469e048c09aa6bd4b69fe4b1c3804', '')
        ],
        left_dictionaries=['myspace.txt'],
        right_dictionaries=['darkweb2017-top1000.txt'],
        left_rule='',
        right_rule=''
    ),
    CombinationTestInput(
        hash_type='sha1',
        hashes=[
            ('75da3d6038c28b57c8b3b34ae2f8121357bae1b9', ''),
            ('6514189a7cbd9c61518d560d67690e08984e26da', ''),
            ('b4130e4e4a9cb4a7ccf58273af14b362aac9563b', ''),
            ('b471d2050dff0fd4d6baf271b8fa72b4755d846d', 'iloveyou14bar'),
            ('fe1a55bca20469e048c09aa6bd4b69fe4b1c3804', '')
        ],
        left_dictionaries=['myspace.txt'],
        right_dictionaries=['bible.txt'],
        left_rule='',
        right_rule=''
    ),
]
