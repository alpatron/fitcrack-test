from __future__ import annotations
from typing import TYPE_CHECKING
from pathlib import Path

import pytest

from page_object.common.exception import WebadminError

if TYPE_CHECKING:
    from page_object.side_bar import SideBar


@pytest.mark.parametrize('test_file_path',[Path('./test/e2e_library/pcfg/fc_auto_test_pcfg_bad_extension.badext')], indirect=True)
def test_file_with_bad_extension_should_be_rejected(test_file_path:Path,side_bar:SideBar):
    pcfg_management = side_bar.goto_pcfg_library()
    with pytest.raises(WebadminError, match=r"This file extension is not allowed."):
        pcfg_management.upload_pcfg(test_file_path)


@pytest.mark.parametrize('test_file_path',
    [
        pytest.param(Path('./test/e2e_library/pcfg/fc_auto_test_pcfg_malformed.zip'), id='has_zip_extension_but_is_not_zip_file'),
        pytest.param(Path('./test/e2e_library/pcfg/fc_auto_test_pcfg_invalid_zip_content.zip'), id='is_zip_file_but_does_contain_PCFG')
    ], indirect=True)
def test_invalid_file_should_be_rejected(test_file_path:Path,side_bar:SideBar):
    pcfg_management = side_bar.goto_pcfg_library()
    with pytest.raises(WebadminError):
        pcfg_management.upload_pcfg(test_file_path)
