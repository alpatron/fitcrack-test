from __future__ import annotations

from enum import Enum

import pytest
from selenium.webdriver.support.wait import WebDriverWait
from page_object.LoginPage import LoginPage
from typing import TYPE_CHECKING, List, Optional
if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver



PREFIX = 'http://192.168.56.2:81'

class HybridMode(Enum):
    MASK_FIRST = 'mask-first'
    DICT_FIRST = 'dict-first'

@pytest.mark.parametrize("hashtype,hashes,dictionaries,rulefiles,min_password_len,max_password_len,min_element_count,max_element_count,keyspace_limit,check_duplicates,case_permutation,random_rule_count", [
    ('sha1', [
        ('a6aea12209b10b7a778aa6f04147f95381777f76','testAbc'),
        ('99efaa0e32d2ce548b466cfe9ae3d0b46c7e5262',''),
        ('0af1b052580d6fae10f6cc1ca598c9e11ca2e155',''),
        ('b8fa77a900fa9aa5341084f2f20cca35552d31a8','aBctest'),
        ],
        ['adobe100.txt'],
        ['toggles1.rule'],
        4,
        7,
        1,
        2,
        None,
        True,
        False,
        0
    )
    ]
    )
def test_prince(selenium:WebDriver,hashtype:str,hashes:List[tuple[str,str]],dictionaries:List[str],rulefiles:List[str],min_password_len:int,max_password_len:int,min_element_count:int,max_element_count:int,keyspace_limit:Optional[int],check_duplicates:bool,case_permutation:bool,random_rule_count:int):
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
    
    prince_settings = attackSettings.choosePrinceMode()

    prince_settings.selectDictionaries(dictionaries)
    prince_settings.selectRulefiles(rulefiles)
    prince_settings.setMinimalPasswordLenght(min_password_len)
    prince_settings.setMaximalPasswordLenght(max_password_len)
    prince_settings.setMinimalNumberOfElementsPerChain(min_element_count)
    prince_settings.setMaximalNumberOfElementsPerChain(max_element_count)
    prince_settings.setPasswordDuplicateCheck(check_duplicates)
    prince_settings.setCasePermutationMode(case_permutation)
    prince_settings.setRandomRuleCount(random_rule_count)
    if keyspace_limit is not None:
        prince_settings.setKeyspaceLimit(keyspace_limit)


    jobDetailPage = jobCreationPage.createJob()

    assert jobDetailPage.get_job_state() == 'Ready'

    jobDetailPage.start_job()

    WebDriverWait(selenium,3600).until(lambda _: jobDetailPage.get_job_state() == 'Finished')

    workedOnHashes = jobDetailPage.getHashes()

    assert set(workedOnHashes) == set(hashes)
