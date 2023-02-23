"""Page object representing a row in the Markov-statistics-file table.
Exports single class--the aforementioned page object.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By

from page_object.table.generic_enableable_table_row import GenericEnableableTableRow

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class MarkovFileSelection(GenericEnableableTableRow):
    """This class represents a row from the markov-file-selection table on the brute-force
    attack settings on the Add Job page."""
    @property
    def __name_field(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(2)')

    @property
    def __added_date(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(3)')

    #TODO: Dunno if I want to use properties for this nonsense.
    @property
    def name(self) -> str:
        """The file name of the Markov statistics file."""
        return self.__name_field.text

    @property
    def added_date(self) -> str:
        """The date this file was added to Fitcrack."""
        return self.__added_date.text
