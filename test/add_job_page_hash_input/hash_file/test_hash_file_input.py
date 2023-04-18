from __future__ import annotations
from typing import TYPE_CHECKING
from pathlib import Path

import pytest


if TYPE_CHECKING:
    from page_object.add_job_page.add_job_page import AddJobPage


HASH_TEST_FILES = [
    Path('./test/add_job_page_hash_input/hash_file/fc_auto_test_hash_file_1.txt').absolute(),
    Path('./test/add_job_page_hash_input/hash_file/fc_auto_test_hash_file_2.txt').absolute(),
]

def test_add_from_file_works(add_job_page:AddJobPage):
    expected_hashes = HASH_TEST_FILES[0].read_text().splitlines() 
    
    input_settings = add_job_page.open_input_settings()
    input_settings.append_hashes_from_hash_file(HASH_TEST_FILES[0])
    
    assert input_settings.get_input_hashes() == expected_hashes

def test_add_from_file_works_two_appends(add_job_page:AddJobPage):
    expected_hashes = HASH_TEST_FILES[0].read_text().splitlines() + HASH_TEST_FILES[1].read_text().splitlines()

    input_settings = add_job_page.open_input_settings()
    input_settings.append_hashes_from_hash_file(HASH_TEST_FILES[0])
    input_settings.append_hashes_from_hash_file(HASH_TEST_FILES[1])
    
    assert input_settings.get_input_hashes() == expected_hashes
