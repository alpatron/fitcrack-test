from __future__ import annotations
from typing import TYPE_CHECKING, List
from dataclasses import dataclass

import pytest

from .conftest import GenericE2ECrackingTestInput

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from page_object.add_job_page.add_job_page import AddJobPage


@dataclass(frozen=True)
class DictionaryTestInput(GenericE2ECrackingTestInput):
    dictionaries:List[str]
    rule_files:List[str]

from .data_test_dictionary import testdata

@pytest.mark.parametrize("testdata", testdata)
def test_dictionary(e2e_cracking_test,selenium:WebDriver,add_job_page:AddJobPage,testdata:DictionaryTestInput):
    attack_settings = add_job_page.open_attack_settings()
    dictionary_settings = attack_settings.choose_dictionary_mode()

    dictionary_settings.select_dictionaries(testdata.dictionaries)
    dictionary_settings.select_rule_files(testdata.rule_files)
