from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional

import pytest

from .conftest import GenericE2ECrackingTestInput

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from page_object.add_job_page.add_job_page import AddJobPage
    from page_object.add_job_page.brute_force_attack_settings import MarkovMode


@dataclass
class BruteForceTestInput(GenericE2ECrackingTestInput):
    masks:List[str]
    custom_charsets:List[str]
    markov_file:Optional[str]
    markov_mode:MarkovMode
    markov_threshold:Optional[int]

from .data_test_bruteforce import testdata

@pytest.mark.parametrize("testdata",testdata)
def test_brute_force(e2e_cracking_test,selenium:WebDriver,add_job_page:AddJobPage,testdata:BruteForceTestInput):
    attack_settings = add_job_page.open_attack_settings()
    brute_force_settings = attack_settings.choose_brute_force_mode()

    brute_force_settings.set_masks_from_list(testdata.masks)
    brute_force_settings.select_charsets(testdata.custom_charsets)
    if testdata.markov_file is not None:
        brute_force_settings.select_markov_file(testdata.markov_file)
    brute_force_settings.select_markov_mode(testdata.markov_mode)
    if testdata.markov_threshold is not None:
        brute_force_settings.set_markov_threshold_value(testdata.markov_threshold)

    brute_force_settings.get_selected_markov_mode()
