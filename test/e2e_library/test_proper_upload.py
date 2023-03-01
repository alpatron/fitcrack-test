from __future__ import annotations
from typing import TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from page_object.side_bar import SideBar

def test_dict_appears_in_list(selenium:WebDriver,side_bar:SideBar):
    dictionary_management = side_bar.goto_dictionary_library()

    dictionary_management.upload_dictionary(str(Path('./test/e2e_library/test_dictionary_correct.txt').absolute()))

    dictionaries_after_upload = dictionary_management.get_available_dictionaries()

    for dictionary in dictionaries_after_upload:
        if dictionary.name == 'test_dictionary_correct.txt':
            return
    assert False