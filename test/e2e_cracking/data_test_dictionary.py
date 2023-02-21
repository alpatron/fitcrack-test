"""Test data for test_dictionary.py"""
from test_dictionary import DictionaryTestInput


testdata = [
    DictionaryTestInput(
        hashtype='sha1',
        hashes=[
            ('c0b51c46e4dcde6189e48ec9695fe55efc0ea703', 'strawberry'),
            ('c0baf4391defd68bf678f0a5ca2b69f828177ddf', ''),
            ('240794c3cd2f7c5be0c58340e2dd33a5518b543a', ''),
            ('e083612b4a67573e1d46743c39878d44e81916cd', ''),
            ('e7b66d3af606d05d40d89bdd18e437a1be28b625', '')
        ],
        dictionaries=['darkweb2017-top1000.txt'],
        rule_files=[]
    ),
    DictionaryTestInput(
        hashtype='sha1',
        hashes=[
            ('c0b51c46e4dcde6189e48ec9695fe55efc0ea703', 'strawberry'),
            ('c0baf4391defd68bf678f0a5ca2b69f828177ddf', 'str@wberry'),
            ('240794c3cd2f7c5be0c58340e2dd33a5518b543a', ''),
            ('e083612b4a67573e1d46743c39878d44e81916cd', ''),
            ('e7b66d3af606d05d40d89bdd18e437a1be28b625', '')
        ],
        dictionaries=['darkweb2017-top1000.txt'],
        rule_files=['leetspeak.rule']
    ),
    DictionaryTestInput(
        hashtype='sha1',
        hashes=[
            ('c0b51c46e4dcde6189e48ec9695fe55efc0ea703', 'strawberry'),
            ('c0baf4391defd68bf678f0a5ca2b69f828177ddf', ''),
            ('240794c3cd2f7c5be0c58340e2dd33a5518b543a', 'strawBerry'),
            ('e083612b4a67573e1d46743c39878d44e81916cd', 'Amanda'),
            ('e7b66d3af606d05d40d89bdd18e437a1be28b625', '')
        ],
        dictionaries=['darkweb2017-top1000.txt'],
        rule_files=['toggles1.rule']
    ),
    DictionaryTestInput(
        hashtype='sha1',
        hashes=[
            ('c0b51c46e4dcde6189e48ec9695fe55efc0ea703', 'strawberry'),
            ('c0baf4391defd68bf678f0a5ca2b69f828177ddf', ''),
            ('240794c3cd2f7c5be0c58340e2dd33a5518b543a', ''),
            ('e083612b4a67573e1d46743c39878d44e81916cd', 'Amanda'),
            ('e7b66d3af606d05d40d89bdd18e437a1be28b625', '')
        ],
        dictionaries=['honeynet.txt'],
        rule_files=[]
    ),
    DictionaryTestInput(
        hashtype='sha1',
        hashes=[
            ('c0b51c46e4dcde6189e48ec9695fe55efc0ea703', 'strawberry'),
            ('c0baf4391defd68bf678f0a5ca2b69f828177ddf', 'str@wberry'),
            ('240794c3cd2f7c5be0c58340e2dd33a5518b543a', ''),
            ('e083612b4a67573e1d46743c39878d44e81916cd', 'Amanda'),
            ('e7b66d3af606d05d40d89bdd18e437a1be28b625', '')
        ],
        dictionaries=['honeynet.txt'],
        rule_files=['leetspeak.rule']
    ),
    DictionaryTestInput(
        hashtype='sha1',
        hashes=[
            ('c0b51c46e4dcde6189e48ec9695fe55efc0ea703', 'strawberry'),
            ('c0baf4391defd68bf678f0a5ca2b69f828177ddf', ''),
            ('240794c3cd2f7c5be0c58340e2dd33a5518b543a', 'strawBerry'),
            ('e083612b4a67573e1d46743c39878d44e81916cd', 'Amanda'),
            ('e7b66d3af606d05d40d89bdd18e437a1be28b625', 'Amanda13')
        ],
        dictionaries=['honeynet.txt'],
        rule_files=['toggles1.rule']
    ),
]
