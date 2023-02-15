from __future__ import annotations
from typing import TYPE_CHECKING, List, NamedTuple

import pytest
from selenium.webdriver.support.wait import WebDriverWait

from page_object.login_page import LoginPage

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from page_object.add_job_page import AddJobPage


class CombinationTestInput(NamedTuple):
    hashtype:str
    hashes:List[tuple[str,str]]
    left_dictionaries:List[str]
    right_dictionaries:List[str]
    left_rule:str
    right_rule:str

from data_test_combination import testdata

@pytest.mark.parametrize("testdata", testdata)
def test_combination(selenium:WebDriver,add_job_page:AddJobPage,testdata:CombinationTestInput):
    inputSettings = add_job_page.open_input_settings()
    inputSettings.select_hash_type_exactly(testdata.hashtype)
    inputSettings.input_hashes_manually([x[0] for x in testdata.hashes])

    attackSettings = add_job_page.open_attack_settings()
    combinationSettings = attackSettings.choose_combination_mode()

    combinationSettings.select_left_dictionaries(testdata.left_dictionaries)
    combinationSettings.select_right_dictionaries(testdata.right_dictionaries)
    combinationSettings.set_left_mangling_rule(testdata.left_rule)
    combinationSettings.set_right_mangling_rule(testdata.right_rule)

    jobDetailPage = add_job_page.create_job()

    assert jobDetailPage.get_job_state() == 'Ready'

    jobDetailPage.start_job()

    WebDriverWait(selenium,3600).until(lambda _: jobDetailPage.get_job_state() == 'Finished')

    workedOnHashes = jobDetailPage.get_hashes()

    assert set(workedOnHashes) == set(testdata.hashes)
