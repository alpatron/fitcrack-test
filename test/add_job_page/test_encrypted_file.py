from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from selenium.webdriver.support.wait import WebDriverWait

from page_object.common.helper import TERMINATING_JOB_STATES

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from page_object.add_job_page.input_settings import InputSettings
    from page_object.add_job_page.add_job_page import AddJobPage

@dataclass(frozen=True)
class EncryptedFileTestInput:
    filepath:Path
    expected_hash:str
    expected_hash_type:str

from .data_test_encrypted_file import TEST_DATA

@pytest.mark.parametrize('test_data',TEST_DATA)
class TestEncryptedFile:
    def test_extraction_did_not_fail(self,input_settings:InputSettings, test_data:EncryptedFileTestInput):
        input_settings.extract_hash_from_file(test_data.filepath)

    def test_output_has_expected_hash(self,input_settings:InputSettings, test_data:EncryptedFileTestInput):
        input_settings.extract_hash_from_file(test_data.filepath)
        extracted_hashes = input_settings.get_input_hashes()
        assert extracted_hashes == [test_data.expected_hash]

    def test_output_has_expected_hash_type(self,input_settings:InputSettings, test_data:EncryptedFileTestInput):
        input_settings.extract_hash_from_file(test_data.filepath)
        hash_type = input_settings.get_selected_hash_type()
        assert hash_type == test_data.expected_hash_type

    def test_extracted_hash_should_get_cracked(self,selenium:WebDriver,add_job_page:AddJobPage,input_settings:InputSettings, test_data:EncryptedFileTestInput):
        input_settings.extract_hash_from_file(test_data.filepath)
        attack_settings = add_job_page.open_attack_settings()
        brute_force_settings = attack_settings.choose_brute_force_mode()
        brute_force_settings.set_masks_from_list(['password'])

        job_detail_page = add_job_page.create_job()
        job_detail_page.start_job()
        WebDriverWait(selenium,600).until(lambda _: job_detail_page.get_job_state() in TERMINATING_JOB_STATES)

        assert job_detail_page.get_hashes()[0][1] == 'password'