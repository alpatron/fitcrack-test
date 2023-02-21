from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING, List
from dataclasses import dataclass

import pytest

from .conftest import GenericE2ECrackingTestInput

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from page_object.add_job_page.add_job_page import AddJobPage


class HybridMode(Enum):
    MASK_FIRST = 'mask-first'
    DICT_FIRST = 'dict-first'


@dataclass(frozen=True)
class HybridTestInput(GenericE2ECrackingTestInput):
    hashes:List[tuple[str,str]]
    mode:HybridMode
    dictionaries:List[str]
    rule:str
    mask:str

from .data_test_hybrid import testdata

@pytest.mark.parametrize("testdata", testdata)
def test_hybrid(e2e_cracking_test,selenium:WebDriver,add_job_page:AddJobPage,testdata:HybridTestInput):    
    attack_settings = add_job_page.open_attack_settings()
    match testdata.mode:
        case HybridMode.DICT_FIRST:
            hybrid_settings = attack_settings.choose_hybrid_wordlist_and_maks_mode()
        case HybridMode.MASK_FIRST:
            hybrid_settings = attack_settings.choose_hybrid_mask_and_wordlist_mode()

    hybrid_settings.select_dictionaries(testdata.dictionaries)
    hybrid_settings.set_mangling_rule(testdata.rule)
    hybrid_settings.set_mask(testdata.mask)
