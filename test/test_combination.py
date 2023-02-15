from __future__ import annotations
from typing import TYPE_CHECKING, List, NamedTuple

import pytest
from selenium.webdriver.support.wait import WebDriverWait

from page_object.login_page import LoginPage

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from .conftest import Credentials


class CombinationTestInput(NamedTuple):
    hashtype:str
    hashes:List[tuple[str,str]]
    left_dictionaries:List[str]
    right_dictionaries:List[str]
    left_rule:str
    right_rule:str

from data_test_combination import testdata

@pytest.mark.parametrize("testdata", testdata)
def test_combination(selenium:WebDriver,base_url:str,credentials:Credentials,testdata:CombinationTestInput):
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
    combinationSettings = attackSettings.choose_combination_mode()

    combinationSettings.select_left_dictionaries(testdata.left_dictionaries)
    combinationSettings.select_right_dictionaries(testdata.right_dictionaries)
    combinationSettings.set_left_mangling_rule(testdata.left_rule)
    combinationSettings.set_right_mangling_rule(testdata.right_rule)

    jobDetailPage = jobCreationPage.create_job()

    assert jobDetailPage.get_job_state() == 'Ready'

    jobDetailPage.start_job()

    WebDriverWait(selenium,3600).until(lambda _: jobDetailPage.get_job_state() == 'Finished')

    workedOnHashes = jobDetailPage.get_hashes()

    assert set(workedOnHashes) == set(testdata.hashes)
