"""Page object representing a row in the PCFG-grammar-file table.
Exports single class--the aforementioned page object.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By

from page_object.generic_table_selection import GenericTableSelection

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class PCFGGrammarSelection(GenericTableSelection):
    """This class represents a row from the PCFG-selection table from the PCFG
    attack settings on the Add Job page."""
    @property
    def __name_field(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(2) a')

    @property
    def __keyspace_field(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(3)')

    @property
    def __added_date_field(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(4)')

    #TODO: Dunno if I want to use properties for this nonsense.
    @property
    def name(self) -> str:
        """The file name of the PCFG-grammar file."""
        return self.__name_field.text

    @property
    def keyspace(self) -> str:
        """The keyspace size of the PCFG-grammar file."""
        return self.__keyspace_field.text

    @property
    def added_date(self) -> str:
        """The date this file was added to Fitcrack."""
        return self.__added_date_field.text
