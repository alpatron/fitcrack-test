from __future__ import annotations
from typing import TYPE_CHECKING
from pathlib import Path

import pytest

from page_object.common.helper import predicate_in_list

if TYPE_CHECKING:
    from page_object.side_bar import SideBar
    from page_object.library.pcfg import PCFGManagement

TEST_FILES = [
    pytest.param(Path('./test/e2e_library/pcfg/fc_auto_test_pcfg_correct.zip'))
]

@pytest.mark.parametrize('test_file_path',TEST_FILES,indirect=True)
class TestPCFGProperUpload:
    @pytest.fixture(autouse=True)
    def pcfg_management(self, test_file_path:Path, side_bar:SideBar) -> PCFGManagement:
        pcfg_management = side_bar.goto_pcfg_library()
        pcfg_management.upload_pcfg(test_file_path)
        return pcfg_management

    def test_upload_did_not_fail(self):
        assert True

    def test_appears_in_list(self,test_file_path:Path,pcfg_management:PCFGManagement):
        assert predicate_in_list(lambda x: x.name == test_file_path.stem, pcfg_management.get_available_pcfgs())
    
    def test_download_gives_same_file(self,test_file_path:Path,test_file_binary_content:bytes,pcfg_management:PCFGManagement):
        uploaded_pcfg = predicate_in_list(lambda x: x.name == test_file_path.stem, pcfg_management.get_available_pcfgs())
        downloaded_file = uploaded_pcfg.download(as_binary=True)

        assert test_file_binary_content == downloaded_file
    
    def test_appears_in_attack_settings(self,test_file_path:Path,side_bar:SideBar):
        add_job_page = side_bar.goto_add_job()
        attack_settings = add_job_page.open_attack_settings()
        pcfg_attack_settings = attack_settings.choose_pcfg_mode()
        predicate_in_list(lambda x: x.name == test_file_path.stem, pcfg_attack_settings.get_available_pcfg_grammars())

    def test_delete(self,test_file_path:Path,pcfg_management:PCFGManagement):
        uploaded_pcfg = predicate_in_list(lambda x: x.name == test_file_path.stem, pcfg_management.get_available_pcfgs())
        uploaded_pcfg.delete()
        with pytest.raises(ValueError):
            predicate_in_list(lambda x: x.name == test_file_path.stem, pcfg_management.get_available_pcfgs())
