from __future__ import annotations

import pytest
from selenium.webdriver.support.wait import WebDriverWait
from page_object.LoginPage import LoginPage
from typing import TYPE_CHECKING, List, Optional
if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver



PREFIX = 'http://192.168.56.2:81'

@pytest.mark.parametrize("hashtype,hashes,grammar,rulefiles,keyspace_limit", [
    ('sha1', [
        ('5254792d5579984f98c41d1858e1722b2dbcc6b3','eminem'),
        ('cfbdc287325676c27264f4208a9cddbbf99f8603',''),
        ('2394eeac9fc3db56189a894e221220b6089e78d3',''),
        ('4597d3842636881e19dd8121a49f5ffa92c56617','didierdemaeyer'),
        ('51abb9636078defbf888d8457a7c76f85c8f114c','')
        ],
        'facebook-pastebay',
        ['best64.rule'],
        None
    )
    ]
    )
def test_pcfg(selenium:WebDriver,hashtype:str,hashes:List[tuple[str,str]],grammar:str,rulefiles:List[str],keyspace_limit:Optional[int]):
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
    pcfg_settings = attackSettings.choosePCFGMode()

    pcfg_settings.selectPCFGGrammar(grammar)
    pcfg_settings.selectRulefiles(rulefiles)
    if keyspace_limit is not None:
        pcfg_settings.set_keyspace_limit(keyspace_limit)

    jobDetailPage = jobCreationPage.createJob()

    assert jobDetailPage.get_job_state() == 'Ready'

    jobDetailPage.start_job()

    WebDriverWait(selenium,3600).until(lambda _: jobDetailPage.get_job_state() == 'Finished')

    workedOnHashes = jobDetailPage.getHashes()

    assert set(workedOnHashes) == set(hashes)
