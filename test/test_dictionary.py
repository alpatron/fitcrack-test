from __future__ import annotations

import pytest
from selenium.webdriver.support.wait import WebDriverWait
from page_object.LoginPage import LoginPage
from typing import TYPE_CHECKING, List
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
    
    jobCreationPage = sidebar.goto_create_job()
    jobCreationPage.setJobName('A fun job for the whole family!')
    
    inputSettings = jobCreationPage.openInputSettings()
    inputSettings.selectHashTypeExactly(hashtype)
    inputSettings.inputHashesManually([x[0] for x in hashes])

    attackSettings = jobCreationPage.openAttackSettings()
    dictionarySettings = attackSettings.chooseDictionaryMode()

    dictionarySettings.selectDictionaries(dictionaries)
    

    jobDetailPage = jobCreationPage.createJob()

    assert jobDetailPage.get_job_state() == 'Ready'

    jobDetailPage.start_job()

    WebDriverWait(selenium,3600).until(lambda _: jobDetailPage.get_job_state() == 'Finished')

    workedOnHashes = jobDetailPage.getHashes()

    assert set(workedOnHashes) == set(hashes)
