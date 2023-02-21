from __future__ import annotations

import pytest
from selenium.webdriver.support.wait import WebDriverWait
from page_object.login_page import LoginPage
from typing import TYPE_CHECKING, List, Optional, NamedTuple
if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from page_object.add_job_page.add_job_page import AddJobPage
    from page_object.add_job_page.brute_force_attack_settings import MarkovMode


class BruteForceTestInput(NamedTuple):
    hashtype:str
    hashes:List[tuple[str,str]]
    masks:List[str]
    custom_charsets:List[str]
    markov_file:Optional[str]
    markov_mode:MarkovMode
    markov_threshold:Optional[int]

from data_test_bruteforce import testdata

@pytest.mark.parametrize("testdata",testdata)
def test_bruteforce(selenium:WebDriver,add_job_page:AddJobPage,testdata:BruteForceTestInput):
    inputSettings = add_job_page.open_input_settings()
    inputSettings.select_hash_type_exactly(testdata.hashtype)
    inputSettings.input_hashes_manually([x[0] for x in testdata.hashes])

    attackSettings = add_job_page.open_attack_settings()
    bruteforceSettings = attackSettings.choose_bruteforce_mode()

    bruteforceSettings.set_masks_from_list(testdata.masks)
    bruteforceSettings.select_charsets(testdata.custom_charsets)
    if testdata.markov_file is not None:
        bruteforceSettings.select_markov_file(testdata.markov_file)
    bruteforceSettings.select_markov_mode(testdata.markov_mode)
    if testdata.markov_threshold is not None:
        bruteforceSettings.set_markov_threshold_value(testdata.markov_threshold)

    bruteforceSettings.get_selected_markov_mode()

    jobDetailPage = add_job_page.create_job()

    assert jobDetailPage.get_job_state() == 'Ready'

    jobDetailPage.start_job()

    WebDriverWait(selenium,3600).until(lambda _: jobDetailPage.get_job_state() == 'Finished')

    workedOnHashes = jobDetailPage.get_hashes()

    assert set(workedOnHashes) == set(testdata.hashes)
