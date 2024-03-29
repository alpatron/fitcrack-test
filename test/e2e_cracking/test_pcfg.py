from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional
from dataclasses import dataclass

import pytest

from .conftest import GenericE2ECrackingTestInput

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from page_object.add_job_page.add_job_page import AddJobPage


@dataclass(frozen=True)
class PCFGTestInput(GenericE2ECrackingTestInput):
    grammar:str
    rule_file:Optional[str]
    keyspace_limit:Optional[int]

from .data_test_pcfg import testdata

@pytest.mark.parametrize('testdata', testdata)
def test_pcfg(e2e_cracking_test,selenium:WebDriver,add_job_page:AddJobPage,testdata:PCFGTestInput):
    attack_settings = add_job_page.open_attack_settings()
    pcfg_settings = attack_settings.choose_pcfg_mode()

    pcfg_settings.select_pcfg_grammar(testdata.grammar)
    if testdata.rule_file is not None:
        pcfg_settings.select_rule_file(testdata.rule_file)
    if testdata.keyspace_limit is not None:
        pcfg_settings.set_keyspace_limit(testdata.keyspace_limit)
