from __future__ import annotations

import pytest
from selenium.webdriver.support.wait import WebDriverWait
from page_object.login_page import LoginPage
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
    
    jobCreationPage = sidebar.goto_add_job()
    jobCreationPage.set_job_name('A fun job for the whole family!')
    
    inputSettings = jobCreationPage.open_input_settings()
    inputSettings.select_hash_type_exactly(hashtype)
    inputSettings.input_hashes_manually([x[0] for x in hashes])

    attackSettings = jobCreationPage.open_attack_settings()
    pcfg_settings = attackSettings.choose_pcfg_mode()

    pcfg_settings.select_pcfg_grammar(grammar)
    pcfg_settings.select_rule_files(rulefiles)
    if keyspace_limit is not None:
        pcfg_settings.set_keyspace_limit(keyspace_limit)

    jobDetailPage = jobCreationPage.create_job()

    assert jobDetailPage.get_job_state() == 'Ready'

    jobDetailPage.start_job()

    WebDriverWait(selenium,3600).until(lambda _: jobDetailPage.get_job_state() == 'Finished')

    workedOnHashes = jobDetailPage.get_hashes()

    assert set(workedOnHashes) == set(hashes)
