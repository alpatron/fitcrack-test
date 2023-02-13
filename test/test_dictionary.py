from __future__ import annotations

import pytest
from selenium.webdriver.support.wait import WebDriverWait
from page_object.login_page import LoginPage
from typing import TYPE_CHECKING, List
from selenium.webdriver import ActionChains
if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver



PREFIX = 'http://192.168.56.2:81'

@pytest.mark.parametrize("hashtype,hashes,dictionaries", [
    ('sha1', [
        ('c0b51c46e4dcde6189e48ec9695fe55efc0ea703','strawberry'),
        ('c0baf4391defd68bf678f0a5ca2b69f828177ddf',''),
        ('240794c3cd2f7c5be0c58340e2dd33a5518b543a',''),
        ('e083612b4a67573e1d46743c39878d44e81916cd',''),
        ('e7b66d3af606d05d40d89bdd18e437a1be28b625','')
        ],
        ['darkweb2017-top1000.txt']
    )
    ]
    )
def test_dictionary(selenium:WebDriver,hashtype:str,hashes:List[tuple[str,str]],dictionaries:List[str]):
    loginPage = LoginPage(selenium,no_ensure_loaded=True)
    loginPage.navigate(PREFIX)
    loginPage.ensure_loaded()

    sidebar, dashboard = loginPage.login('fitcrack','FITCRACK')
    
    jobCreationPage = sidebar.goto_add_job()
    jobCreationPage.set_job_name('A fun job for the whole family!')
    
    inputSettings = jobCreationPage.open_input_settings()
    inputSettings.select_hash_type_exactly(hashtype)
    inputSettings.input_hashes_manually([x[0] for x in hashes])

    attackSettings = jobCreationPage.open_attack_settings()
    dictionarySettings = attackSettings.choose_dictionary_mode()


    dictionarySettings.select_dictionaries(dictionaries)
    

    jobDetailPage = jobCreationPage.create_job()

    assert jobDetailPage.get_job_state() == 'Ready'

    jobDetailPage.start_job()

    WebDriverWait(selenium,3600).until(lambda _: jobDetailPage.get_job_state() == 'Finished')

    workedOnHashes = jobDetailPage.get_hashes()

    assert set(workedOnHashes) == set(hashes)
