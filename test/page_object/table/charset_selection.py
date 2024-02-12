"""Page object representing a row in a charset-selection table.
Exports single class--the aforementioned page object.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By

from page_object.table.generic_enableable_table_row import GenericEnableableTableRow

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class CharsetSelection(GenericEnableableTableRow):
    """This class represents a row from the charset-selection table on the brute-force
    attack settings on the Add Job page.
    """
    @property
    def __name_field(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(2) a')

    @property
    def __keyspace_field(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(3)')

    @property
    def name(self) -> str:
        """The file name of the charset."""
        return self.__name_field.text

    @property
    def keyspace(self) -> str:
        """The keyspace size of the charset."""
        return self.__keyspace_field.text
   