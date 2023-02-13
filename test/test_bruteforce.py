from __future__ import annotations

import pytest
from selenium.webdriver.support.wait import WebDriverWait
from page_object.login_page import LoginPage
from page_object.brute_force_settings import MarkovMode
from typing import TYPE_CHECKING, List, Optional, NamedTuple
if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver

PREFIX = 'http://192.168.56.2:81'

class BruteForceTestInput(NamedTuple):
    hashtype:str
    hashes:List[tuple[str,str]]
    masks:List[str]
    custom_charsets:List[str]
    markov_file:Optional[str]
    markov_mode_raw:str
    markov_threshold:Optional[int]

from data_test_bruteforce import testdata

@pytest.mark.parametrize("testdata",testdata)
def test_bruteforce(selenium:WebDriver,testdata:BruteForceTestInput):
    markov_mode = MarkovMode(testdata.markov_mode_raw)
    
    loginPage = LoginPage(selenium,no_ensure_loaded=True)
    loginPage.navigate(PREFIX)
    loginPage.ensure_loaded()

    sidebar, dashboard = loginPage.login('fitcrack','FITCRACK')
    
    jobCreationPage = sidebar.goto_add_job()
    jobCreationPage.set_job_name('A fun job for the whole family!')
    
    inputSettings = jobCreationPage.open_input_settings()
    inputSettings.select_hash_type_exactly(testdata.hashtype)
    inputSettings.input_hashes_manually([x[0] for x in testdata.hashes])

    attackSettings = jobCreationPage.open_attack_settings()
    bruteforceSettings = attackSettings.choose_bruteforce_mode()

    bruteforceSettings.set_masks_from_list(testdata.masks)
    bruteforceSettings.select_charsets(testdata.custom_charsets)
    if testdata.markov_file is not None:
        bruteforceSettings.select_markov_file(testdata.markov_file)
    bruteforceSettings.select_markov_mode(markov_mode)
    if testdata.markov_threshold is not None:
        bruteforceSettings.set_markov_threshold_value(testdata.markov_threshold)

    bruteforceSettings.get_selected_markov_mode()

    jobDetailPage = jobCreationPage.create_job()

    assert jobDetailPage.get_job_state() == 'Ready'

    jobDetailPage.start_job()

    WebDriverWait(selenium,3600).until(lambda _: jobDetailPage.get_job_state() == 'Finished')

    workedOnHashes = jobDetailPage.get_hashes()

    assert set(workedOnHashes) == set(testdata.hashes)
