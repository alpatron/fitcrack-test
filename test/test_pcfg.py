from __future__ import annotations

import pytest
from selenium.webdriver.support.wait import WebDriverWait
from page_object.login_page import LoginPage
from typing import TYPE_CHECKING, List, Optional, NamedTuple
if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from page_object.add_job_page.add_job_page import AddJobPage


class PCFGTestInput(NamedTuple):
    hashtype:str
    hashes:List[tuple[str,str]]
    grammar:str
    rulefiles:List[str]
    keyspace_limit:Optional[int]

from data_test_pcfg import testdata

@pytest.mark.parametrize('testdata', testdata)
def test_pcfg(selenium:WebDriver,add_job_page:AddJobPage,testdata:PCFGTestInput):
    inputSettings = add_job_page.open_input_settings()
    inputSettings.select_hash_type_exactly(testdata.hashtype)
    inputSettings.input_hashes_manually([x[0] for x in testdata.hashes])

    attackSettings = add_job_page.open_attack_settings()
    pcfg_settings = attackSettings.choose_pcfg_mode()

    pcfg_settings.select_pcfg_grammar(testdata.grammar)
    pcfg_settings.select_rule_files(testdata.rulefiles)
    if testdata.keyspace_limit is not None:
        pcfg_settings.set_keyspace_limit(testdata.keyspace_limit)

    jobDetailPage = add_job_page.create_job()

    assert jobDetailPage.get_job_state() == 'Ready'

    jobDetailPage.start_job()

    WebDriverWait(selenium,3600).until(lambda _: jobDetailPage.get_job_state() == 'Finished')

    workedOnHashes = jobDetailPage.get_hashes()

    assert set(workedOnHashes) == set(testdata.hashes)
