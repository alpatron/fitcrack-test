from __future__ import annotations
from typing import TYPE_CHECKING, List
from dataclasses import dataclass

import pytest

from .conftest import GenericE2ECrackingTestInput

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from page_object.add_job_page.add_job_page import AddJobPage


@dataclass
class CombinationTestInput(GenericE2ECrackingTestInput):
    left_dictionaries:List[str]
    right_dictionaries:List[str]
    left_rule:str
    right_rule:str

from .data_test_combination import testdata

@pytest.mark.parametrize("testdata", testdata)
def test_combination(e2e_cracking_test,selenium:WebDriver,add_job_page:AddJobPage,testdata:CombinationTestInput):
    attack_settings = add_job_page.open_attack_settings()
    combination_settings = attack_settings.choose_combination_mode()

    combination_settings.select_left_dictionaries(testdata.left_dictionaries)
    combination_settings.select_right_dictionaries(testdata.right_dictionaries)
    combination_settings.set_left_mangling_rule(testdata.left_rule)
    combination_settings.set_right_mangling_rule(testdata.right_rule)
