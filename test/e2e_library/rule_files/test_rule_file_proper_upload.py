from __future__ import annotations
from typing import TYPE_CHECKING
from pathlib import Path

import pytest

from  page_object.common.helper import predicate_in_list

if TYPE_CHECKING:
    from page_object.side_bar import SideBar
    from page_object.library.rules import RuleFileManagement

TEST_FILES = [
    pytest.param(Path('./test/e2e_library/rule_files/fc_auto_test_rule_file_correct.txt'),id='file_ext_txt'),
    pytest.param(Path('./test/e2e_library/rule_files/fc_auto_test_rule_file_correct.rule'),id='file_ext_rule')
]

@pytest.mark.parametrize('test_file_path',TEST_FILES,indirect=True)
class TestRuleFileProperUpload:
    @pytest.fixture(autouse=True)
    def rule_file_management(self, test_file_path:Path, side_bar:SideBar) -> RuleFileManagement:
        rule_file_management = side_bar.goto_rule_file_library()
        rule_file_management.upload_rule_file(test_file_path)
        return rule_file_management

    def test_upload_did_not_fail(self):
        assert True

    def test_rule_appears_in_list(self,test_file_path:Path,rule_file_management:RuleFileManagement):
        assert predicate_in_list(lambda x: x.name == test_file_path.name, rule_file_management.get_available_rule_files())

    def test_download_gives_same_file(self,test_file_path:Path,test_file_text_content:str,rule_file_management:RuleFileManagement):
        uploaded_rule_file = predicate_in_list(lambda x: x.name == test_file_path.name, rule_file_management.get_available_rule_files())
        downloaded_file = uploaded_rule_file.download()

        assert test_file_text_content == downloaded_file

    def test_rule_file_appears_in_attack_settings(self,test_file_path:Path,side_bar:SideBar):
        add_job_page = side_bar.goto_add_job()
        attack_settings = add_job_page.open_attack_settings()
        dictionary_attack_settings = attack_settings.choose_dictionary_mode()
        assert dictionary_attack_settings.rule_file_with_name_exists(test_file_path.name)

    def test_delete(self,test_file_path:Path,rule_file_management:RuleFileManagement):
        uploaded_rule_file = predicate_in_list(lambda x: x.name == test_file_path.name, rule_file_management.get_available_rule_files())
        uploaded_rule_file.delete()
        with pytest.raises(ValueError):
            predicate_in_list(lambda x: x.name == test_file_path.name, rule_file_management.get_available_rule_files())
