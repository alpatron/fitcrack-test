from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    import _pytest.fixtures

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

    def test_extracted_hash_should_get_cracked(self,add_job_page:AddJobPage,input_settings:InputSettings, test_data:EncryptedFileTestInput,request:_pytest.fixtures.FixtureRequest):
        add_job_page.set_job_name(f'Job created by an automatic Fitcrack test -- {request.node.name} -- {datetime.utcnow().isoformat()}')

        input_settings.extract_hash_from_file(test_data.filepath)
        attack_settings = add_job_page.open_attack_settings()
        brute_force_settings = attack_settings.choose_brute_force_mode()
        brute_force_settings.set_masks_from_list(['password'])

        job_detail_page = add_job_page.create_job()
        job_detail_page.start_job()
        job_detail_page.wait_until_job_finished(600)

        assert job_detail_page.get_hashes()[0][1] == 'password'