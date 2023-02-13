from __future__ import annotations

from enum import Enum

import pytest
from selenium.webdriver.support.wait import WebDriverWait
from page_object.login_page import LoginPage
from typing import TYPE_CHECKING, List
from selenium.webdriver import ActionChains
if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver



PREFIX = 'http://192.168.56.2:81'

class HybridMode(Enum):
    MASK_FIRST = 'mask-first'
    DICT_FIRST = 'dict-first'

@pytest.mark.parametrize("hashtype,hashes,mode_raw,dictionaries,rule,mask", [
    ('sha1', [
        ('06a3f6380a7f9a76462e2edbdaefe718eb9ea033',''),
        ('0085411372df2865c07d45c20345caedbfdae958',''),
        ('2e7359ed0f945aeab3bae275f3d1f487451ed48b',''),
        ('3650c195b6eb82db3818ec19c7c055b6f91b9675',''),
        ('341b5129bf9b6abcbd96ecaf158506090f9d77b5','')
        ],
        'mask-first',
        ['honeynet.txt'],
        'c $-',
        '?l?l?l'
    )
    ]
    )
def test_hybrid(selenium:WebDriver,hashtype:str,hashes:List[tuple[str,str]],mode_raw:str,dictionaries:List[str],rule:str,mask:str):
    mode = HybridMode(mode_raw)
    
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
    match mode:
        case HybridMode.DICT_FIRST:
            hybridSettings = attackSettings.choose_hybrid_wordlist_and_maks_mode()
        case HybridMode.MASK_FIRST:
            hybridSettings = attackSettings.choose_hybrid_mask_and_wordlist_mode()

    hybridSettings.select_dictionaries(dictionaries)
    hybridSettings.set_mangling_rule(rule)
    hybridSettings.set_mask(mask)

    jobDetailPage = jobCreationPage.create_job()

    assert jobDetailPage.get_job_state() == 'Ready'

    jobDetailPage.start_job()

    WebDriverWait(selenium,3600).until(lambda _: jobDetailPage.get_job_state() == 'Finished')

    workedOnHashes = jobDetailPage.get_hashes()

    assert set(workedOnHashes) == set(hashes)
