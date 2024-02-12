from __future__ import annotations
from typing import TYPE_CHECKING
from pathlib import Path

import pytest

from page_object.common.helper import predicate_in_list

if TYPE_CHECKING:
    from page_object.side_bar import SideBar
    from page_object.library.markov import MarkovFileManagement

TEST_FILES = [
    pytest.param(Path('./test/e2e_library/dictionary/fc_auto_test_dictionary_correct.txt'))
]

@pytest.mark.parametrize('test_file_path',TEST_FILES,indirect=True)
class TestMarkovFromDictionary:
    @pytest.fixture(autouse=True)
    def markov_file_management(self, test_file_path:Path, side_bar:SideBar) -> MarkovFileManagement:
        dictionary_management = side_bar.goto_dictionary_library()
        dictionary_management.upload_dictionary(test_file_path)
        markov_file_management = side_bar.goto_markov_file_library()
        markov_file_management.make_markov_file_from_dictionary(test_file_path.name)
        return markov_file_management

    def test_creation_did_not_fail(self):
        assert True

    def test_appears_in_list(self,test_file_path:Path,markov_file_management:MarkovFileManagement):
        assert predicate_in_list(lambda x: x.name == test_file_path.with_suffix('.hcstat2').name, markov_file_management.get_available_markov_files())

    def test_appears_in_attack_settings(self,test_file_path:Path,side_bar:SideBar):
        add_job_page = side_bar.goto_add_job()
        attack_settings = add_job_page.open_attack_settings()
        brute_force_attack_settings = attack_settings.choose_brute_force_mode()
        predicate_in_list(lambda x: x.name == test_file_path.with_suffix('.hcstat2').name, brute_force_attack_settings.get_available_markov_files())

    def test_delete(self,test_file_path:Path,markov_file_management:MarkovFileManagement):
        uploaded_markov_file = predicate_in_list(lambda x: x.name == test_file_path.with_suffix('.hcstat2').name, markov_file_management.get_available_markov_files())
        uploaded_markov_file.delete()
        with pytest.raises(ValueError):
            predicate_in_list(lambda x: x.name == test_file_path.with_suffix('.hcstat2').name, markov_file_management.get_available_markov_files())
