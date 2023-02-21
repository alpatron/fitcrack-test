"""Test data for test_bruteforce.py"""
from test_bruteforce import BruteForceTestInput
from page_object.add_job_page.brute_force_attack_settings import MarkovMode

testdata = [
    BruteForceTestInput(
        hashtype='sha1',
        hashes=[
            ('9282dbcb46212929fcc2bdfcc4836ea694465dc7', 'ZDARXX'),
            ('26b0da18d000abc9f5804395cb5bcfe22f253151', 'AAABBB'),
            ('9b241b7f3c3764b9dee00e7a07da6cad48d891c9', 'ANANAN'),
            ('2176ec59dfe01e1e3251efbd0b23aa52f4ea33b0', 'BAAAAA'),
            ('413725d25c4f7f624ef10fabebbe97dd5800de96', 'MANIER')
        ],
        masks=['?u?u?u?u?u?u'],
        custom_charsets=[],
        markov_file=None,
        markov_mode=MarkovMode.MARKOV_DISABLED,
        markov_threshold=None
    ),
    BruteForceTestInput(
        hashtype='sha1',
        hashes=[
            ('9282dbcb46212929fcc2bdfcc4836ea694465dc7', 'ZDARXX'),
            ('26b0da18d000abc9f5804395cb5bcfe22f253151', 'AAABBB'),
            ('9b241b7f3c3764b9dee00e7a07da6cad48d891c9', 'ANANAN'),
            ('2176ec59dfe01e1e3251efbd0b23aa52f4ea33b0', 'BAAAAA'),
            ('413725d25c4f7f624ef10fabebbe97dd5800de96', 'MANIER')
        ],
        masks=['?u?u?u?u?u?u'],
        custom_charsets=[],
        markov_file='hashcat.hcstat2',
        markov_mode=MarkovMode.MARKOV_2D,
        markov_threshold=None
    ),
    BruteForceTestInput(
        hashtype='sha1',
        hashes=[
            ('9282dbcb46212929fcc2bdfcc4836ea694465dc7', ''),
            ('26b0da18d000abc9f5804395cb5bcfe22f253151', ''),
            ('9b241b7f3c3764b9dee00e7a07da6cad48d891c9', 'ANANAN'),
            ('2176ec59dfe01e1e3251efbd0b23aa52f4ea33b0', ''),
            ('413725d25c4f7f624ef10fabebbe97dd5800de96', '')
        ],
        masks=['?u?u?u?u?u?u'],
        custom_charsets=[],
        markov_file='hashcat.hcstat2',
        markov_mode=MarkovMode.MARKOV_2D,
        markov_threshold=7
    ),
    BruteForceTestInput(
        hashtype='sha1',
        hashes=[
            ('9282dbcb46212929fcc2bdfcc4836ea694465dc7', ''),
            ('26b0da18d000abc9f5804395cb5bcfe22f253151', 'AAABBB'),
            ('9b241b7f3c3764b9dee00e7a07da6cad48d891c9', ''),
            ('2176ec59dfe01e1e3251efbd0b23aa52f4ea33b0', ''),
            ('413725d25c4f7f624ef10fabebbe97dd5800de96', '')
        ],
        masks=['?u?u?u?u?u?u'],
        custom_charsets=[],
        markov_file='adobe100.hcstat2',
        markov_mode=MarkovMode.MARKOV_2D,
        markov_threshold=7
    ),
    BruteForceTestInput(
        hashtype='sha1',
        hashes=[
            ('9282dbcb46212929fcc2bdfcc4836ea694465dc7', 'ZDARXX'),
            ('26b0da18d000abc9f5804395cb5bcfe22f253151', 'AAABBB'),
            ('9b241b7f3c3764b9dee00e7a07da6cad48d891c9', 'ANANAN'),
            ('2176ec59dfe01e1e3251efbd0b23aa52f4ea33b0', 'BAAAAA'),
            ('413725d25c4f7f624ef10fabebbe97dd5800de96', 'MANIER')
        ],
        masks=['?u?u?u?u?u?u'],
        custom_charsets=[],
        markov_file='hashcat.hcstat2',
        markov_mode=MarkovMode.MARKOV_3D,
        markov_threshold=None
    ),
    BruteForceTestInput(
        hashtype='sha1',
        hashes=[
            ('9282dbcb46212929fcc2bdfcc4836ea694465dc7', ''),
            ('26b0da18d000abc9f5804395cb5bcfe22f253151', ''),
            ('9b241b7f3c3764b9dee00e7a07da6cad48d891c9', 'ANANAN'),
            ('2176ec59dfe01e1e3251efbd0b23aa52f4ea33b0', ''),
            ('413725d25c4f7f624ef10fabebbe97dd5800de96', 'MANIER')
        ],
        masks=['?u?u?u?u?u?u'],
        custom_charsets=[],
        markov_file='hashcat.hcstat2',
        markov_mode=MarkovMode.MARKOV_3D,
        markov_threshold=7
    ),
    BruteForceTestInput(
        hashtype='sha1',
        hashes=[
            ('9282dbcb46212929fcc2bdfcc4836ea694465dc7', ''),
            ('26b0da18d000abc9f5804395cb5bcfe22f253151', 'AAABBB'),
            ('9b241b7f3c3764b9dee00e7a07da6cad48d891c9', ''),
            ('2176ec59dfe01e1e3251efbd0b23aa52f4ea33b0', 'BAAAAA'),
            ('413725d25c4f7f624ef10fabebbe97dd5800de96', '')
        ],
        masks=['?u?u?u?u?u?u'],
        custom_charsets=[],
        markov_file='adobe100.hcstat2',
        markov_mode=MarkovMode.MARKOV_3D,
        markov_threshold=7
    ),
    BruteForceTestInput(
        hashtype='sha1',
        hashes=[
            ('b26940e5e462f4d4767933d02e870b00b884d0c5', 'HEX<bbc8cdcf>'),
        ],
        masks=['?u?u?u?u?u?u'],
        custom_charsets=['cz_ISO-8859-2.hcchr'],
        markov_file=None,
        markov_mode=MarkovMode.MARKOV_DISABLED,
        markov_threshold=None
    ),
]
