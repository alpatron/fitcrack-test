from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional
from dataclasses import dataclass

import pytest

from .conftest import GenericE2ECrackingTestInput

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from page_object.add_job_page.add_job_page import AddJobPage


@dataclass(frozen=True)
class PRINCETestInput(GenericE2ECrackingTestInput):
    dictionaries:List[str]
    rule_file:Optional[str]
    min_password_len:int
    max_password_len:int
    min_element_count:int
    max_element_count:int
    keyspace_limit:Optional[int]
    check_duplicates:bool
    case_permutation:bool
    random_rule_count:int

from .data_test_prince import testdata

@pytest.mark.parametrize('testdata', testdata)
def test_prince(e2e_cracking_test,selenium:WebDriver,add_job_page:AddJobPage,testdata:PRINCETestInput):
    attackSettings = add_job_page.open_attack_settings()
    
    prince_settings = attackSettings.choose_prince_mode()

    prince_settings.select_dictionaries(testdata.dictionaries)
    if testdata.rule_file is not None:
        prince_settings.select_rule_file(testdata.rule_file)
    prince_settings.set_minimal_password_length(testdata.min_password_len)
    prince_settings.set_maximal_password_length(testdata.max_password_len)
    prince_settings.set_minimal_number_of_elements_per_chain(testdata.min_element_count)
    prince_settings.set_maximal_number_of_elements_per_chain(testdata.max_element_count)
    prince_settings.set_password_duplicate_check(testdata.check_duplicates)
    prince_settings.set_case_permutation_mode(testdata.case_permutation)
    prince_settings.set_random_rule_count(testdata.random_rule_count)
    if testdata.keyspace_limit is not None:
        prince_settings.set_keyspace_limit(testdata.keyspace_limit)
