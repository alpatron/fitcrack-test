from __future__ import annotations
from typing import TYPE_CHECKING
from pathlib import Path
from datetime import datetime
import shutil

import pytest


if TYPE_CHECKING:
    from page_object.side_bar import SideBar
    from page_object.library.rules import RuleFileManagement


class TestRuleFileProperUpload:
    
    RAW_TEST_TXT_FILE_NAME = Path('fc_auto_test_rule_file_correct.txt')
    RAW_TEST_TXT_FILE_PATH = Path('./test/e2e_library/rule_files/').joinpath(RAW_TEST_TXT_FILE_NAME).absolute()
    
    RAW_TEST_RULE_FILE_NAME = Path('fc_auto_test_rule_file_correct.rule')
    RAW_TEST_RULE_FILE_PATH = Path('./test/e2e_library/rule_files/').joinpath(RAW_TEST_TXT_FILE_NAME).absolute()

    @pytest.fixture(autouse=True)
    def prepare_test_file(self):
        self.TEST_TXT_FILE_NAME = self.RAW_TEST_TXT_FILE_NAME.with_stem(f'{self.RAW_TEST_TXT_FILE_NAME.stem}-{datetime.utcnow().strftime("%Y%m%d%H%M%S")}')
        self.TEST_TXT_FILE_PATH = self.RAW_TEST_TXT_FILE_PATH.with_name(self.TEST_TXT_FILE_NAME.name)
        self.TEST_RULE_FILE_NAME = self.RAW_TEST_RULE_FILE_NAME.with_stem(f'{self.RAW_TEST_TXT_FILE_NAME.stem}-{datetime.utcnow().strftime("%Y%m%d%H%M%S")}')
        self.TEST_RULE_FILE_PATH = self.RAW_TEST_RULE_FILE_PATH.with_name(self.TEST_RULE_FILE_NAME.name)
        shutil.copyfile(self.RAW_TEST_TXT_FILE_PATH,self.TEST_TXT_FILE_PATH)
        shutil.copyfile(self.RAW_TEST_RULE_FILE_PATH,self.TEST_RULE_FILE_PATH)
        with open(self.TEST_TXT_FILE_PATH,'r') as file:
            self.TEST_FILE_CONTENT = file.read()
        yield
        self.TEST_TXT_FILE_PATH.unlink()
        self.TEST_RULE_FILE_PATH.unlink()

    @pytest.fixture
    def rule_file_management(self, prepare_test_file, side_bar:SideBar) -> RuleFileManagement:
        rule_file_management = side_bar.goto_rule_file_library()
        return rule_file_management
    
    @pytest.fixture
    def upload_txt_file(self,rule_file_management:RuleFileManagement):
        rule_file_management.upload_rule_file(self.TEST_TXT_FILE_PATH)

    @pytest.fixture
    def upload_rule_file(self,rule_file_management:RuleFileManagement):
        rule_file_management.upload_rule_file(self.TEST_RULE_FILE_PATH)

    def test_upload_did_not_fail_txt_ext(self,upload_txt_file):
        assert True

    def test_upload_did_not_fail_rule_ext(self,upload_rule_file):
        assert True

    def test_rule_appears_in_list_txt_ext(self,upload_txt_file,rule_file_management:RuleFileManagement):
        assert rule_file_management.rule_file_with_name_exists(self.TEST_TXT_FILE_NAME.name)
    
    def test_rule_appears_in_list_rule_ext(self,upload_rule_file,rule_file_management:RuleFileManagement):
        assert rule_file_management.rule_file_with_name_exists(self.TEST_RULE_FILE_NAME.name)
    
    def test_download_gives_same_file_txt_ext(self,upload_txt_file,rule_file_management:RuleFileManagement):
        uploaded_rule_file = rule_file_management.get_rule_file_with_name(self.TEST_TXT_FILE_NAME.name)
        downloaded_file = uploaded_rule_file.download(as_binary=True)

        assert self.TEST_FILE_CONTENT == downloaded_file

    def test_download_gives_same_file_rule_ext(self,upload_rule_file,rule_file_management:RuleFileManagement):
        uploaded_rule_file = rule_file_management.get_rule_file_with_name(self.TEST_RULE_FILE_NAME.name)
        downloaded_file = uploaded_rule_file.download(as_binary=True)

        assert self.TEST_FILE_CONTENT == downloaded_file
    
    def test_rule_file_appears_in_attack_settings_txt_ext(self,upload_txt_file,side_bar:SideBar):
        add_job_page = side_bar.goto_add_job()
        attack_settings = add_job_page.open_attack_settings()
        dictionary_attack_settings = attack_settings.choose_dictionary_mode()
        assert dictionary_attack_settings.rule_file_with_name_exists(self.TEST_TXT_FILE_NAME.name)

    def test_rule_file_appears_in_attack_settings_rule_ext(self,upload_rule_file,side_bar:SideBar):
        add_job_page = side_bar.goto_add_job()
        attack_settings = add_job_page.open_attack_settings()
        dictionary_attack_settings = attack_settings.choose_dictionary_mode()
        assert dictionary_attack_settings.rule_file_with_name_exists(self.TEST_RULE_FILE_NAME.name)

    def test_delete_txt_ext(self,upload_txt_file,rule_file_management:RuleFileManagement):
        uploaded_rule_file = rule_file_management.get_rule_file_with_name(self.TEST_TXT_FILE_NAME.name)
        uploaded_rule_file.delete()
        assert not rule_file_management.rule_file_with_name_exists(self.TEST_TXT_FILE_NAME.name)

    def test_delete_rule_ext(self,upload_rule_file,rule_file_management:RuleFileManagement):
        uploaded_rule_file = rule_file_management.get_rule_file_with_name(self.TEST_TXT_FILE_NAME.name)
        uploaded_rule_file.delete()
        assert not rule_file_management.rule_file_with_name_exists(self.TEST_TXT_FILE_NAME.name)
