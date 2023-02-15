from __future__ import annotations

from enum import Enum

import pytest
from selenium.webdriver.support.wait import WebDriverWait
from page_object.login_page import LoginPage
from typing import TYPE_CHECKING, List, NamedTuple
if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from page_object.add_job_page import AddJobPage

class HybridTestInput(NamedTuple):
    hashtype:str
    hashes:List[tuple[str,str]]
    mode_raw:str
    dictionaries:List[str]
    rule:str
    mask:str

from test_combination import testdata


class HybridMode(Enum):
    MASK_FIRST = 'mask-first'
    DICT_FIRST = 'dict-first'


@pytest.mark.parametrize("testdata", testdata)
def test_hybrid(selenium:WebDriver,add_job_page:AddJobPage,testdata:HybridTestInput):
    mode = HybridMode(testdata.mode_raw)
    
    inputSettings = add_job_page.open_input_settings()
    inputSettings.select_hash_type_exactly(testdata.hashtype)
    inputSettings.input_hashes_manually([x[0] for x in testdata.hashes])

    attackSettings = add_job_page.open_attack_settings()
    match mode:
        case HybridMode.DICT_FIRST:
            hybridSettings = attackSettings.choose_hybrid_wordlist_and_maks_mode()
        case HybridMode.MASK_FIRST:
            hybridSettings = attackSettings.choose_hybrid_mask_and_wordlist_mode()

    hybridSettings.select_dictionaries(testdata.dictionaries)
    hybridSettings.set_mangling_rule(testdata.rule)
    hybridSettings.set_mask(testdata.mask)

    jobDetailPage = add_job_page.create_job()

    assert jobDetailPage.get_job_state() == 'Ready'

    jobDetailPage.start_job()

    WebDriverWait(selenium,3600).until(lambda _: jobDetailPage.get_job_state() == 'Finished')

    workedOnHashes = jobDetailPage.get_hashes()

    assert set(workedOnHashes) == set(testdata.hashes)
