from __future__ import annotations
from typing import TYPE_CHECKING
from pathlib import Path
from datetime import datetime
import shutil

import pytest

from page_object.common.exception import WebadminError

if TYPE_CHECKING:
    from page_object.side_bar import SideBar

class TestDictionaryMalformedUploads:

    RAW_TEST_FILE_NAME = Path('fc_auto_test_dictionary_bad_extension.badext')
    RAW_TEST_FILE_PATH = Path('./test/e2e_library/').joinpath(RAW_TEST_FILE_NAME).absolute()

    @pytest.fixture()
    def prepare_test_file(self):
        self.TEST_FILE_NAME = self.RAW_TEST_FILE_NAME.with_stem(f'{self.RAW_TEST_FILE_NAME.stem}-{datetime.utcnow().strftime("%Y%m%d%H%M%S")}')
        self.TEST_FILE_PATH = self.RAW_TEST_FILE_PATH.with_name(self.TEST_FILE_NAME.name)
        shutil.copyfile(self.RAW_TEST_FILE_PATH,self.TEST_FILE_PATH)
        yield
        self.TEST_FILE_PATH.unlink()

    def test_file_with_bad_extension_should_be_rejected(self,prepare_test_file,side_bar:SideBar):
        dictionary_management = side_bar.goto_dictionary_library()
        with pytest.raises(WebadminError, match=r"This file extension is not allowed."):
            dictionary_management.upload_dictionary(self.TEST_FILE_PATH)