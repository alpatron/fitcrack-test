from __future__ import annotations
from typing import TYPE_CHECKING
from pathlib import Path

import pytest

from page_object.common.helper import predicate_in_list

if TYPE_CHECKING:
    from page_object.side_bar import SideBar
    from page_object.library.mask import MaskManagement

TEST_FILES = [
    pytest.param(Path('./test/e2e_library/mask/fc_auto_test_mask_file_correct.txt'),id='file_ext_txt'),
    pytest.param(Path('./test/e2e_library/mask/fc_auto_test_mask_file_correct.hcmask'),id='file_ext_hcmask'),
]

TEST_MASKS = [
    '?l',
    '?l?l',
    '?l?l?l',
    '?l?l?l?l',
    '?l?l?l?l?l',
    '?l?l?l?l?l?l',
    '?l?l?l?l?l?l?l',
    '?l?l?l?l?l?l?l?l',
    '?l?l?l?l?l?l?l?l?l',
    '?l?l?l?l?l?l?l?l?l?l',
    '' #Empty string at the end because WebAdmin appends an empty mask after the loaded ones.
]

@pytest.mark.parametrize('test_file_path',TEST_FILES,indirect=True)
class TestMaskProperUpload:
    @pytest.fixture(autouse=True)
    def mask_management(self, test_file_path:Path, side_bar:SideBar) -> MaskManagement:
        mask_management = side_bar.goto_mask_library()
        mask_management.upload_mask(test_file_path)
        return mask_management

    def test_upload_did_not_fail(self):
        assert True

    def test_appears_in_list(self,test_file_path:Path,mask_management:MaskManagement):
        assert predicate_in_list(lambda x: x.name == test_file_path.name, mask_management.get_available_mask_files())
    
    def test_download_gives_same_file(self,test_file_path:Path,test_file_text_content:str,mask_management:MaskManagement):
        uploaded_mask_file = predicate_in_list(lambda x: x.name == test_file_path.name, mask_management.get_available_mask_files())
        downloaded_file = uploaded_mask_file.download()

        assert test_file_text_content == downloaded_file
    
    def test_appears_in_attack_settings(self,test_file_path:Path,side_bar:SideBar):
        add_job_page = side_bar.goto_add_job()
        attack_settings = add_job_page.open_attack_settings()
        brute_force_attack_settings = attack_settings.choose_brute_force_mode()
        brute_force_attack_settings.get_available_mask_files().index(test_file_path.name) #Will throw exception on failure, causing the test to fail should there be a problem

    def test_masks_can_be_loaded_in_attack_settings(self,test_file_path:Path,side_bar:SideBar):
        add_job_page = side_bar.goto_add_job()
        attack_settings = add_job_page.open_attack_settings()
        brute_force_attack_settings = attack_settings.choose_brute_force_mode()
        brute_force_attack_settings.load_mask_file(test_file_path.name)
        assert brute_force_attack_settings.get_all_input_masks() == TEST_MASKS

    def test_delete(self,test_file_path:Path,mask_management:MaskManagement):
        uploaded_mask_file = predicate_in_list(lambda x: x.name == test_file_path.name,mask_management.get_available_mask_files())
        uploaded_mask_file.delete()
        with pytest.raises(ValueError):
            predicate_in_list(lambda x: x.name == test_file_path.stem, mask_management.get_available_mask_files())
