"""Test data for test_prince.py"""
from __future__ import annotations
from .test_prince import PRINCETestInput

testdata = [
    PRINCETestInput(
        hash_type='sha1',
        hashes=[
            ('22fa6121da96f43a106e413e65d4f9089c53824c', ''),
            ('a51dda7c7ff50b61eaea0444371f4a6a9301e501', 'john'),
            ('6e017b5464f820a6c1bb5e9f6d711a667a80d8ea', 'heslo'),
            ('ee51e142b0a4fb057d9bb1b8098b6c767c951992', ''),
            ('431364b6450fc47ccdbf6a2205dfdb1baeb79412', 'oracle'),
            ('5855e3590ac1021bf3a894a851c6cc3f52bc2e5d', ''),
            ('86c60296fa8751a5376d75f3a4fc7cef7d20e5b0', 'sunjohn')
        ],
        dictionaries=['honeynet.txt'],
        rule_files=[],
        min_password_len=4,
        max_password_len=7,
        min_element_count=1,
        max_element_count=2,
        keyspace_limit=None,
        check_duplicates=True,
        case_permutation=False,
        random_rule_count=0
    ),
    PRINCETestInput(
        hash_type='sha1',
        hashes=[
            ('f5f6a8e1a321eb4c46e14159a6120952f302e828', 'SunSun'),
            ('0832bccfc73b4d805820820933a3c92db4652a5a', 'Sunjohn')
        ],
        dictionaries=['honeynet.txt'],
        rule_files=[],
        min_password_len=6,
        max_password_len=7,
        min_element_count=2,
        max_element_count=2,
        keyspace_limit=None,
        check_duplicates=True,
        case_permutation=True,
        random_rule_count=0
    ),
    PRINCETestInput(
        hash_type='sha1',
        hashes=[
            ('a6aea12209b10b7a778aa6f04147f95381777f76', 'testAbc'),
            ('99efaa0e32d2ce548b466cfe9ae3d0b46c7e5262', ''),
            ('0af1b052580d6fae10f6cc1ca598c9e11ca2e155', ''),
            ('b8fa77a900fa9aa5341084f2f20cca35552d31a8', 'aBctest')
        ],
        dictionaries=['adobe100.txt'],
        rule_files=['toggles1.rule'],
        min_password_len=4,
        max_password_len=7,
        min_element_count=1,
        max_element_count=2,
        keyspace_limit=None,
        check_duplicates=True,
        case_permutation=False,
        random_rule_count=0
    ),
]
