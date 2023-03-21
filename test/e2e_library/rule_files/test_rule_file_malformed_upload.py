from __future__ import annotations
from typing import TYPE_CHECKING
from pathlib import Path

import pytest

from page_object.common.exception import WebadminError

if TYPE_CHECKING:
    from page_object.side_bar import SideBar

TEST_FILES = [
    Path('./test/e2e_library/rule_files/fc_auto_test_rule_file_bad_extension.badext')
]

@pytest.mark.parametrize('test_file_path',TEST_FILES, indirect=True)
def test_file_with_bad_extension_should_be_rejected(test_file_path:Path,side_bar:SideBar):
    rule_file_management = side_bar.goto_rule_file_library()
    with pytest.raises(WebadminError, match=r"This file extension is not allowed."):
        rule_file_management.upload_rule_file(test_file_path)