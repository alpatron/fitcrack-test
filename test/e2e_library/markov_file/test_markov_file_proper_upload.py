from __future__ import annotations
from typing import TYPE_CHECKING
from pathlib import Path

import pytest

from page_object.common.helper import predicate_in_list

if TYPE_CHECKING:
    from page_object.side_bar import SideBar
    from page_object.library.markov import MarkovFileManagement

TEST_FILES = [
    pytest.param(Path('./test/e2e_library/markov_file/fc_auto_test_markov_file_correct.hcstat2'))
]

@pytest.mark.parametrize('test_file_path',TEST_FILES,indirect=True)
class TestMarkovFileProperUpload:
    @pytest.fixture(autouse=True)
    def markov_file_management(self, test_file_path:Path, side_bar:SideBar) -> MarkovFileManagement:
        markov_file_management = side_bar.goto_markov_file_library()
        markov_file_management.upload_markov_file(test_file_path)
        return markov_file_management

    def test_upload_did_not_fail(self):
        assert True

    def test_appears_in_list(self,test_file_path:Path,markov_file_management:MarkovFileManagement):
        assert predicate_in_list(lambda x: x.name == test_file_path.name, markov_file_management.get_available_markov_files())

    def test_download_gives_same_file(self,test_file_path:Path,test_file_binary_content:bytes,markov_file_management:MarkovFileManagement):
        uploaded_markov_file = predicate_in_list(lambda x: x.name == test_file_path.name, markov_file_management.get_available_markov_files())
        downloaded_file = uploaded_markov_file.download(as_binary=True)

        assert test_file_binary_content == downloaded_file

    def test_appears_in_attack_settings(self,test_file_path:Path,side_bar:SideBar):
        add_job_page = side_bar.goto_add_job()
        attack_settings = add_job_page.open_attack_settings()
        brute_force_attack_settings = attack_settings.choose_brute_force_mode()
        predicate_in_list(lambda x: x.name == test_file_path.name, brute_force_attack_settings.get_available_markov_files())

    def test_delete(self,test_file_path:Path,markov_file_management:MarkovFileManagement):
        uploaded_markov_file = predicate_in_list(lambda x: x.name == test_file_path.name, markov_file_management.get_available_markov_files())
        uploaded_markov_file.delete()
        with pytest.raises(ValueError):
            predicate_in_list(lambda x: x.name == test_file_path.name, markov_file_management.get_available_markov_files())
