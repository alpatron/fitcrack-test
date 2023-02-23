"""Page object representing a row in a dictionary-selection table.
Exports single class--the aforementioned page object.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By

from page_object.table.generic_enableable_table_row import GenericEnableableTableRow

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class DictionarySelection(GenericEnableableTableRow):
    """This class represents a row from the dictionary-selection table on the Add Job screen."""

    @property
    def __name_field(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(2) a')

    @property
    def __keyspace_field(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(3)')

    #TODO: Dunno if I want to use properties for this nonsense.
    @property
    def name(self) -> str:
        """The file name of the dictionary."""
        return self.__name_field.text

    @property
    def keyspace(self) -> str:
        """The keyspace size of the dictionary."""
        return self.__keyspace_field.text
   