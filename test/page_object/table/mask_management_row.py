from __future__ import annotations
from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By

from page_object.table.generic_library_table import GenericLibraryTableRow

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class MaskManagementRow(GenericLibraryTableRow):
    @property
    def __time_field(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(2)')
    
    @property
    def time(self) -> str:
        return self.__time_field.text
