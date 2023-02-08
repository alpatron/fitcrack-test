from __future__ import annotations

from selenium.webdriver.common.by import By
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement

from page_object.GenericTableSelection import GenericTableSelection

class PCFGGrammarSelection(GenericTableSelection):
    '''This class represents a row from the PCFG-selection table from the PCFG-attack settings on the Add Job page.'''
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
        return self.__name_field.text

    @property
    def keyspace(self) -> str:
        return self.__keyspace_field.text
   
    @property
    def added_date(self) -> str:
        return self.__added_date_field.text