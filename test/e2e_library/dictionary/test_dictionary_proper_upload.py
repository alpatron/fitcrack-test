from __future__ import annotations
from typing import TYPE_CHECKING
from pathlib import Path

import pytest

if TYPE_CHECKING:
    from page_object.side_bar import SideBar
    from page_object.library.dictionary import DictionaryManagement


TEST_FILES = [
    Path('./test/e2e_library/dictionary/fc_auto_test_dictionary_correct.txt')
]

@pytest.mark.parametrize('test_file_path',TEST_FILES, indirect=True)
class TestDictionaryProperUpload:
    @pytest.fixture(autouse=True)
    def dictionary_management_after_upload(self, test_file_path:Path,side_bar:SideBar) -> DictionaryManagement:
        dictionary_management = side_bar.goto_dictionary_library()
        dictionary_management.upload_dictionary(test_file_path)
        return dictionary_management
    
    def test_upload_did_not_fail(self):
        assert True

    def test_dict_appears_in_list(self,test_file_path:Path,dictionary_management_after_upload:DictionaryManagement):
        assert dictionary_management_after_upload.dictionary_with_name_exists(test_file_path.name)
    
    def test_download_gives_same_file(self,test_file_path:Path,test_file_text_content:str,dictionary_management_after_upload:DictionaryManagement):
        uploaded_dictionary = dictionary_management_after_upload.get_dictionary_with_name(test_file_path.name)
        downloaded_file = uploaded_dictionary.download()

        assert test_file_text_content == downloaded_file
    
    def test_dictionary_appears_in_attack_settings(self,test_file_path:Path,side_bar:SideBar):
        add_job_page = side_bar.goto_add_job()
        attack_settings = add_job_page.open_attack_settings()
        dictionary_attack_settings = attack_settings.choose_dictionary_mode()
        assert dictionary_attack_settings.dictionary_with_name_exists(test_file_path.name)

    def test_delete(self,test_file_path:Path,dictionary_management_after_upload:DictionaryManagement):
        uploaded_dictionary = dictionary_management_after_upload.get_dictionary_with_name(test_file_path.name)
        uploaded_dictionary.delete()
        assert not dictionary_management_after_upload.dictionary_with_name_exists(test_file_path.name)
