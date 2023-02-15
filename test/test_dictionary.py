from __future__ import annotations

import pytest
from selenium.webdriver.support.wait import WebDriverWait
from page_object.login_page import LoginPage
from typing import TYPE_CHECKING, List, NamedTuple
if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from page_object.add_job_page import AddJobPage



class DictionaryTestInput(NamedTuple):
    hashtype:str
    hashes:List[tuple[str,str]]
    dictionaries:List[str]
    rule_files:List[str]

from data_test_dictionary import testdata

@pytest.mark.parametrize("testdata", testdata)
def test_dictionary(selenium:WebDriver,add_job_page:AddJobPage,testdata:DictionaryTestInput):
    inputSettings = add_job_page.open_input_settings()
    inputSettings.select_hash_type_exactly(testdata.hashtype)
    inputSettings.input_hashes_manually([x[0] for x in testdata.hashes])

    attackSettings = add_job_page.open_attack_settings()
    dictionarySettings = attackSettings.choose_dictionary_mode()


    dictionarySettings.select_dictionaries(testdata.dictionaries)
    dictionarySettings.select_rule_files(testdata.rule_files)

    jobDetailPage = add_job_page.create_job()

    assert jobDetailPage.get_job_state() == 'Ready'

    jobDetailPage.start_job()

    WebDriverWait(selenium,3600).until(lambda _: jobDetailPage.get_job_state() == 'Finished')

    workedOnHashes = jobDetailPage.get_hashes()

    assert set(workedOnHashes) == set(testdata.hashes)
