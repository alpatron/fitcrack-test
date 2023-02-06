from __future__ import annotations

import pytest
from selenium.webdriver.support.wait import WebDriverWait
from page_object.LoginPage import LoginPage
from typing import TYPE_CHECKING, List
from selenium.webdriver import ActionChains
if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver

PREFIX = 'http://192.168.56.2:81'


@pytest.mark.parametrize("hashtype,hashes,left_dictionaries,right_dictionaries,left_rule,right_rule", [
    ('sha1', [
        ('75da3d6038c28b57c8b3b34ae2f8121357bae1b9',''),
        ('6514189a7cbd9c61518d560d67690e08984e26da',''),
        ('b4130e4e4a9cb4a7ccf58273af14b362aac9563b','Matrix-SECRET!!!'),
        ('b471d2050dff0fd4d6baf271b8fa72b4755d846d',''),
        ('fe1a55bca20469e048c09aa6bd4b69fe4b1c3804','')
        ],
        ['english.txt'],
        ['darkweb2017-top1000.txt'],
        'c $-',
        'u $! $! $!'
    )
    ]
    )
def test_combination(selenium:WebDriver,hashtype:str,hashes:List[tuple[str,str]],left_dictionaries:List[str],right_dictionaries:List[str],left_rule:str,right_rule:str):
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
    combinationSettings = attackSettings.chooseCombinationMode()

    combinationSettings.selectLeftDictionaries(left_dictionaries)
    combinationSettings.selectRightDictionaries(right_dictionaries)
    combinationSettings.setLeftManglingRule(left_rule)
    combinationSettings.setRightManglingRule(right_rule)

    jobDetailPage = jobCreationPage.createJob()

    assert jobDetailPage.get_job_state() == 'Ready'

    jobDetailPage.start_job()

    WebDriverWait(selenium,3600).until(lambda _: jobDetailPage.get_job_state() == 'Finished')

    workedOnHashes = jobDetailPage.getHashes()

    assert set(workedOnHashes) == set(hashes)
