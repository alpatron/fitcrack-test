from __future__ import annotations

import pytest
from selenium.webdriver.support.wait import WebDriverWait
from page_object.login_page import LoginPage
from page_object.brute_force_settings import MarkovMode
from typing import TYPE_CHECKING, List, Optional
if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver

PREFIX = 'http://192.168.56.2:81'


@pytest.mark.parametrize("hashtype,hashes,masks,custom_charsets,markov_file,markov_mode_raw,markov_threshold", [
    ('sha1', [
        ('9282dbcb46212929fcc2bdfcc4836ea694465dc7',''),
        ('26b0da18d000abc9f5804395cb5bcfe22f253151',''),
        ('9b241b7f3c3764b9dee00e7a07da6cad48d891c9','ANANAN'),
        ('2176ec59dfe01e1e3251efbd0b23aa52f4ea33b0',''),
        ('413725d25c4f7f624ef10fabebbe97dd5800de96','')
        ],
        ['?u?u?u?u?u?u'],
        [],
        'hashcat.hcstat2',
        'markov-2d',
        7
    )
    ]
    )
def test_bruteforce(selenium:WebDriver,hashtype:str,hashes:List[tuple[str,str]],masks:List[str],custom_charsets:List[str],markov_file:Optional[str],markov_mode_raw:str,markov_threshold:Optional[int]):
    markov_mode = MarkovMode(markov_mode_raw)
    
    loginPage = LoginPage(selenium,no_ensure_loaded=True)
    loginPage.navigate(PREFIX)
    loginPage.ensure_loaded()

    sidebar, dashboard = loginPage.login('fitcrack','FITCRACK')
    
    jobCreationPage = sidebar.goto_add_job()
    jobCreationPage.set_job_name('A fun job for the whole family!')
    
    inputSettings = jobCreationPage.open_input_settings()
    inputSettings.select_hash_type_exactly(hashtype)
    inputSettings.input_hashes_manually([x[0] for x in hashes])

    attackSettings = jobCreationPage.open_attack_settings()
    bruteforceSettings = attackSettings.choose_bruteforce_mode()

    bruteforceSettings.set_masks_from_list(masks)
    bruteforceSettings.select_charsets(custom_charsets)
    if markov_file is not None:
        bruteforceSettings.select_markov_file(markov_file)
    bruteforceSettings.select_markov_mode(markov_mode)
    if markov_threshold is not None:
        bruteforceSettings.set_markov_threshold_value(markov_threshold)

    bruteforceSettings.get_selected_markov_mode()

    jobDetailPage = jobCreationPage.create_job()

    assert jobDetailPage.get_job_state() == 'Ready'

    jobDetailPage.start_job()

    WebDriverWait(selenium,3600).until(lambda _: jobDetailPage.get_job_state() == 'Finished')

    workedOnHashes = jobDetailPage.get_hashes()

    assert set(workedOnHashes) == set(hashes)
