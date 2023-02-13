from __future__ import annotations

from enum import Enum

import pytest
from selenium.webdriver.support.wait import WebDriverWait
from page_object.login_page import LoginPage
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
    
    jobCreationPage = sidebar.goto_add_job()
    jobCreationPage.set_job_name('A fun job for the whole family!')
    
    inputSettings = jobCreationPage.open_input_settings()
    inputSettings.select_hash_type_exactly(hashtype)
    inputSettings.input_hashes_manually([x[0] for x in hashes])

    attackSettings = jobCreationPage.open_attack_settings()
    
    prince_settings = attackSettings.choose_prince_mode()

    prince_settings.select_dictionaries(dictionaries)
    prince_settings.select_rule_files(rulefiles)
    prince_settings.set_minimal_password_length(min_password_len)
    prince_settings.set_maximal_password_length(max_password_len)
    prince_settings.set_minimal_number_of_elements_per_chain(min_element_count)
    prince_settings.set_maximal_number_of_elements_per_chain(max_element_count)
    prince_settings.set_password_duplicate_check(check_duplicates)
    prince_settings.set_case_permutation_mode(case_permutation)
    prince_settings.set_random_rule_count(random_rule_count)
    if keyspace_limit is not None:
        prince_settings.set_keyspace_limit(keyspace_limit)


    jobDetailPage = jobCreationPage.create_job()

    assert jobDetailPage.get_job_state() == 'Ready'

    jobDetailPage.start_job()

    WebDriverWait(selenium,3600).until(lambda _: jobDetailPage.get_job_state() == 'Finished')

    workedOnHashes = jobDetailPage.get_hashes()

    assert set(workedOnHashes) == set(hashes)
