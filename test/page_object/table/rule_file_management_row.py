from __future__ import annotations
from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By

from page_object.table.generic_library_table_row import GenericLibraryTableRow

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class RuleFileManagementRow(GenericLibraryTableRow):
    @property
    def __count_field(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(2)')

    @property
    def __time_field(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(3)')

    @property
    def count(self) -> str:
        return self.__count_field.text

    @property
    def time(self) -> str:
        return self.__time_field.text
