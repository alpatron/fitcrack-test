from __future__ import annotations

import pytest
from selenium.webdriver.support.wait import WebDriverWait
from page_object.LoginPage import LoginPage
from page_object.BruteforceAttackSettings import MarkovMode
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
    
    jobCreationPage = sidebar.goto_create_job()
    jobCreationPage.setJobName('A fun job for the whole family!')
    
    inputSettings = jobCreationPage.openInputSettings()
    inputSettings.selectHashTypeExactly(hashtype)
    inputSettings.inputHashesManually([x[0] for x in hashes])

    attackSettings = jobCreationPage.openAttackSettings()
    bruteforceSettings = attackSettings.chooseBruteforceMode()

    bruteforceSettings.setMasksFromList(masks)
    bruteforceSettings.selectCharsets(custom_charsets)
    if markov_file is not None:
        bruteforceSettings.selectMarkovFile(markov_file)
    bruteforceSettings.selectMarkovMode(markov_mode)
    if markov_threshold is not None:
        bruteforceSettings.setMarkovThresholdValue(markov_threshold)

    bruteforceSettings.getSelectedMarkovMode()

    jobDetailPage = jobCreationPage.createJob()

    assert jobDetailPage.get_job_state() == 'Ready'

    jobDetailPage.start_job()

    WebDriverWait(selenium,3600).until(lambda _: jobDetailPage.get_job_state() == 'Finished')

    workedOnHashes = jobDetailPage.getHashes()

    assert set(workedOnHashes) == set(hashes)
