from __future__ import annotations
from typing import TYPE_CHECKING
from pathlib import Path

import pytest

from page_object.common.helper import predicate_in_list

if TYPE_CHECKING:
    from page_object.side_bar import SideBar
    from page_object.library.charset import CharsetManagement

TEST_FILES = [
    pytest.param(Path('./test/e2e_library/charsets/fc_auto_test_charset_correct.txt'),id='file_ext_txt'),
    pytest.param(Path('./test/e2e_library/charsets/fc_auto_test_charset_correct.charset'),id='file_ext_charset'),
    pytest.param(Path('./test/e2e_library/charsets/fc_auto_test_charset_correct.hcchr'),id='file_ext_hcchr')
]

@pytest.mark.parametrize('test_file_path',TEST_FILES,indirect=True)
class TestCharsetProperUpload:
    @pytest.fixture(autouse=True)
    def charset_management(self, test_file_path:Path, side_bar:SideBar) -> CharsetManagement:
        charset_management = side_bar.goto_charset_library()
        charset_management.upload_charset(test_file_path)
        return charset_management

    def test_upload_did_not_fail(self):
        assert True

    def test_charset_appears_in_list(self,test_file_path:Path,charset_management:CharsetManagement):
        assert predicate_in_list(lambda x: x.name == test_file_path.stem, charset_management.get_available_charset_files())

    def test_download_gives_same_file(self,test_file_path:Path,test_file_text_content:str,charset_management:CharsetManagement):
        uploaded_charset = predicate_in_list(lambda x: x.name == test_file_path.stem, charset_management.get_available_charset_files())
        downloaded_file = uploaded_charset.download()

        assert test_file_text_content == downloaded_file

    def test_charset_appears_in_attack_settings(self,test_file_path:Path,side_bar:SideBar):
        add_job_page = side_bar.goto_add_job()
        attack_settings = add_job_page.open_attack_settings()
        brute_force_attack_settings = attack_settings.choose_brute_force_mode()
        assert predicate_in_list(lambda x: x.name == test_file_path.stem, brute_force_attack_settings.get_available_charsets())

    def test_delete(self,test_file_path:Path,charset_management:CharsetManagement):
        uploaded_charset = predicate_in_list(lambda x: x.name == test_file_path.stem, charset_management.get_available_charset_files())
        uploaded_charset.delete()
        with pytest.raises(ValueError):
            predicate_in_list(lambda x: x.name == test_file_path.stem, charset_management.get_available_charset_files())
