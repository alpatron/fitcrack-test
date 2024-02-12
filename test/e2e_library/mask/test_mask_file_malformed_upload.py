from __future__ import annotations
from typing import TYPE_CHECKING
from pathlib import Path

import pytest

from page_object.common.exception import WebadminError

if TYPE_CHECKING:
    from page_object.side_bar import SideBar

@pytest.mark.parametrize('test_file_path',[Path('./test/e2e_library/mask/fc_auto_test_mask_bad_extension.badext')], indirect=True)
def test_file_with_bad_extension_should_be_rejected(test_file_path:Path,side_bar:SideBar):
    mask_management = side_bar.goto_mask_library()
    with pytest.raises(WebadminError, match=r"This file extension is not allowed."):
        mask_management.upload_mask_file(test_file_path)

@pytest.mark.parametrize('test_file_path',
    [
        pytest.param(Path('./test/e2e_library/mask/fc_auto_test_mask_invalid_mask.txt'),id='ext_txt'),
        pytest.param(Path('./test/e2e_library/mask/fc_auto_test_mask_invalid_mask.hcmask'),id='ext_hcmask')
    ], indirect=True)
def test_file_with_invalid_masks_should_be_rejected(test_file_path:Path,side_bar:SideBar):
    mask_management = side_bar.goto_mask_library()
    with pytest.raises(WebadminError, match=r'Wrong mask'):
        mask_management.upload_mask_file(test_file_path)
