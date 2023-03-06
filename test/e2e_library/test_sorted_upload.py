from __future__ import annotations
from typing import TYPE_CHECKING
from pathlib import Path
from datetime import datetime
import shutil

import pytest


if TYPE_CHECKING:
    from page_object.side_bar import SideBar
    from page_object.library.dictionary.dictionary_management import DictionaryManagement


class TestSortedUpload:
    
    RAW_TEST_FILE_UNSORTED_NAME = Path('fc_auto_test_dictionary_unsorted.txt')
    RAW_TEST_FILE_UNSORTED_PATH = Path('./test/e2e_library/').joinpath(RAW_TEST_FILE_UNSORTED_NAME).absolute()
    
    TEST_FILE_SORTED_PATH = Path('./test/e2e_library/fc_auto_test_dictionary_sorted.txt')

    @pytest.fixture(autouse=True)
    def prepare_test_file(self):
            self.TEST_FILE_UNSORTED_NAME = self.RAW_TEST_FILE_UNSORTED_NAME.with_stem(f'{self.RAW_TEST_FILE_UNSORTED_NAME.stem}-{datetime.utcnow().strftime("%Y%m%d%H%M%S")}')
            self.TEST_FILE_UNSORTED_PATH = self.RAW_TEST_FILE_UNSORTED_PATH.with_name(self.TEST_FILE_UNSORTED_NAME.name)
            shutil.copyfile(self.RAW_TEST_FILE_UNSORTED_PATH,self.TEST_FILE_UNSORTED_PATH)
            with open(self.TEST_FILE_SORTED_PATH,'r') as file:
                self.TEST_FILE_SORTED_CONTENT = file.read()
            yield
            self.TEST_FILE_UNSORTED_PATH.unlink()

    @pytest.fixture(autouse=True)
    def dictionary_management(self, prepare_test_file, side_bar:SideBar) -> DictionaryManagement:
        dictionary_management = side_bar.goto_dictionary_library()
        dictionary_management.upload_dictionary(self.TEST_FILE_UNSORTED_PATH,sort_on_upload=True)
        return dictionary_management
    
    def test_upload_did_not_fail(self):
        assert True

    def test_dict_appears_in_list(self,dictionary_management:DictionaryManagement):
        assert dictionary_management.dictionary_with_name_exists(self.TEST_FILE_UNSORTED_NAME.name)
    
    def test_download_gives_sorted_file(self,dictionary_management:DictionaryManagement):
        uploaded_dictionary = dictionary_management.get_dictionary_with_name(self.TEST_FILE_UNSORTED_NAME.name)
        downloaded_file = uploaded_dictionary.download()

        assert self.TEST_FILE_SORTED_CONTENT == downloaded_file
    
    def test_dictionary_appears_in_attack_settings(self,side_bar:SideBar):
        add_job_page = side_bar.goto_add_job()
        attack_settings = add_job_page.open_attack_settings()
        dictionary_attack_settings = attack_settings.choose_dictionary_mode()
        assert dictionary_attack_settings.dictionary_with_name_exists(self.TEST_FILE_UNSORTED_NAME.name)

    def test_delete(self,dictionary_management:DictionaryManagement):
        uploaded_dictionary = dictionary_management.get_dictionary_with_name(self.TEST_FILE_UNSORTED_NAME.name)
        uploaded_dictionary.delete()
        assert not dictionary_management.dictionary_with_name_exists(self.TEST_FILE_UNSORTED_NAME.name)
