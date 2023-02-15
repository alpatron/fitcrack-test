from __future__ import annotations

from enum import Enum

import pytest
from selenium.webdriver.support.wait import WebDriverWait
from page_object.login_page import LoginPage
from typing import TYPE_CHECKING, List, Optional, NamedTuple
if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from .conftest import Credentials


class PRINCETestInput(NamedTuple):
    hashtype:str
    hashes:List[tuple[str,str]]
    dictionaries:List[str]
    rulefiles:List[str]
    min_password_len:int
    max_password_len:int
    min_element_count:int
    max_element_count:int
    keyspace_limit:Optional[int]
    check_duplicates:bool
    case_permutation:bool
    random_rule_count:int

from data_test_prince import testdata

@pytest.mark.parametrize('testdata', testdata)
def test_prince(selenium:WebDriver,base_url:str,credentials:Credentials,testdata:PRINCETestInput):
    loginPage = LoginPage(selenium,no_ensure_loaded=True)
    loginPage.navigate(base_url)
    loginPage.ensure_loaded()

    sidebar, dashboard = loginPage.login(*credentials)
    
    jobCreationPage = sidebar.goto_add_job()
    jobCreationPage.set_job_name('A fun job for the whole family!')
    
    inputSettings = jobCreationPage.open_input_settings()
    inputSettings.select_hash_type_exactly(testdata.hashtype)
    inputSettings.input_hashes_manually([x[0] for x in testdata.hashes])

    attackSettings = jobCreationPage.open_attack_settings()
    
    prince_settings = attackSettings.choose_prince_mode()

    prince_settings.select_dictionaries(testdata.dictionaries)
    prince_settings.select_rule_files(testdata.rulefiles)
    prince_settings.set_minimal_password_length(testdata.min_password_len)
    prince_settings.set_maximal_password_length(testdata.max_password_len)
    prince_settings.set_minimal_number_of_elements_per_chain(testdata.min_element_count)
    prince_settings.set_maximal_number_of_elements_per_chain(testdata.max_element_count)
    prince_settings.set_password_duplicate_check(testdata.check_duplicates)
    prince_settings.set_case_permutation_mode(testdata.case_permutation)
    prince_settings.set_random_rule_count(testdata.random_rule_count)
    if testdata.keyspace_limit is not None:
        prince_settings.set_keyspace_limit(testdata.keyspace_limit)


    jobDetailPage = jobCreationPage.create_job()

    assert jobDetailPage.get_job_state() == 'Ready'

    jobDetailPage.start_job()

    WebDriverWait(selenium,3600).until(lambda _: jobDetailPage.get_job_state() == 'Finished')

    workedOnHashes = jobDetailPage.get_hashes()

    assert set(workedOnHashes) == set(testdata.hashes)
