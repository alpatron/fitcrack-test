"""Test data for test_hybrid.py"""
from test_hybrid import HybridTestInput


testdata = [
    HybridTestInput(
        hashtype='sha1',
        hashes=[
            ('06a3f6380a7f9a76462e2edbdaefe718eb9ea033', 'jurgen420'),
            ('0085411372df2865c07d45c20345caedbfdae958', ''),
            ('2e7359ed0f945aeab3bae275f3d1f487451ed48b', ''),
            ('3650c195b6eb82db3818ec19c7c055b6f91b9675', 'bart123'),
            ('341b5129bf9b6abcbd96ecaf158506090f9d77b5', 'bart825')
        ],
        mode_raw='wordlist-first',
        dictionaries=['honeynet.txt'],
        rule='',
        mask='?d?d?d'
    ),
    HybridTestInput(
        hashtype='sha1',
        hashes=[
            ('06a3f6380a7f9a76462e2edbdaefe718eb9ea033', ''),
            ('0085411372df2865c07d45c20345caedbfdae958', ''),
            ('2e7359ed0f945aeab3bae275f3d1f487451ed48b', 'heyjurgen'),
            ('3650c195b6eb82db3818ec19c7c055b6f91b9675', ''),
            ('341b5129bf9b6abcbd96ecaf158506090f9d77b5', 'bart825')
        ],
        mode_raw='mask-first',
        dictionaries=['honeynet.txt'],
        rule='',
        mask='?l?l?l'
    ),
    HybridTestInput(
        hashtype='sha1',
        hashes=[
            ('06a3f6380a7f9a76462e2edbdaefe718eb9ea033', ''),
            ('0085411372df2865c07d45c20345caedbfdae958', ''),
            ('2e7359ed0f945aeab3bae275f3d1f487451ed48b', ''),
            ('3650c195b6eb82db3818ec19c7c055b6f91b9675', ''),
            ('341b5129bf9b6abcbd96ecaf158506090f9d77b5', '')
        ],
        mode_raw='mask-first',
        dictionaries=['honeynet.txt'],
        rule='c $-',
        mask='?l?l?l'
    ),
]
