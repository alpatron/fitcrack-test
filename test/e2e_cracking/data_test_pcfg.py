"""Test data for test_pcfg.py"""
from __future__ import annotations
from .test_pcfg import PCFGTestInput


testdata = [
    PCFGTestInput(
        hash_type='sha1',
        hashes=[
            ('5254792d5579984f98c41d1858e1722b2dbcc6b3', 'eminem'),
            ('cfbdc287325676c27264f4208a9cddbbf99f8603', ''),
            ('2394eeac9fc3db56189a894e221220b6089e78d3', ''),
            ('4597d3842636881e19dd8121a49f5ffa92c56617', 'didierdemaeyer'),
            ('51abb9636078defbf888d8457a7c76f85c8f114c', '')
        ],
        grammar='facebook-pastebay',
        rule_files=[],
        keyspace_limit=None
    ),
    PCFGTestInput(
        hash_type='sha1',
        hashes=[
            ('5254792d5579984f98c41d1858e1722b2dbcc6b3', ''),
            ('cfbdc287325676c27264f4208a9cddbbf99f8603', ''),
            ('2394eeac9fc3db56189a894e221220b6089e78d3', 'amanda'),
            ('4597d3842636881e19dd8121a49f5ffa92c56617', ''),
            ('51abb9636078defbf888d8457a7c76f85c8f114c', '')
        ],
        grammar='twitter-banned',
        rule_files=[],
        keyspace_limit=None
    ),
    PCFGTestInput(
        hash_type='sha1',
        hashes=[
            ('5254792d5579984f98c41d1858e1722b2dbcc6b3', ''),
            ('cfbdc287325676c27264f4208a9cddbbf99f8603', ''),
            ('2394eeac9fc3db56189a894e221220b6089e78d3', ''),
            ('4597d3842636881e19dd8121a49f5ffa92c56617', ''),
            ('51abb9636078defbf888d8457a7c76f85c8f114c', '')
        ],
        grammar='john',
        rule_files=[],
        keyspace_limit=None,
        wait_time=3600
    ),
    PCFGTestInput(
        hash_type='sha1',
        hashes=[
            ('5254792d5579984f98c41d1858e1722b2dbcc6b3', 'eminem'),
            ('cfbdc287325676c27264f4208a9cddbbf99f8603', ''),
            ('2394eeac9fc3db56189a894e221220b6089e78d3', ''),
            ('4597d3842636881e19dd8121a49f5ffa92c56617', 'didierdemaeyer'),
            ('51abb9636078defbf888d8457a7c76f85c8f114c', '')
        ],
        grammar='facebook-pastebay',
        rule_files=['best64.rule'],
        keyspace_limit=None
    ),
    PCFGTestInput(
        hash_type='sha1',
        hashes=[
            ('5254792d5579984f98c41d1858e1722b2dbcc6b3', ''),
            ('cfbdc287325676c27264f4208a9cddbbf99f8603', ''),
            ('2394eeac9fc3db56189a894e221220b6089e78d3', 'amanda'),
            ('4597d3842636881e19dd8121a49f5ffa92c56617', ''),
            ('51abb9636078defbf888d8457a7c76f85c8f114c', '')
        ],
        grammar='twitter-banned',
        rule_files=['leetspeak.rule'],
        keyspace_limit=None
    ),
    PCFGTestInput(
        hash_type='sha1',
        hashes=[
            ('5254792d5579984f98c41d1858e1722b2dbcc6b3', ''),
            ('cfbdc287325676c27264f4208a9cddbbf99f8603', ''),
            ('2394eeac9fc3db56189a894e221220b6089e78d3', ''),
            ('4597d3842636881e19dd8121a49f5ffa92c56617', ''),
            ('51abb9636078defbf888d8457a7c76f85c8f114c', '')
        ],
        grammar='john',
        rule_files=['toggles1.rule'],
        keyspace_limit=None,
        wait_time=3600
    ),
]
