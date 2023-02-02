from __future__ import annotations

from selenium.webdriver.common.by import By
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement

from page_object.GenericTableSelection import GenericTableSelection

class DictionarySelection(GenericTableSelection):
    '''
    This class represents a row from the dictionary-selection table on the Job Creation screen.
    '''
    @property
    def __name_field(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(2) a')

    @property
    def __keyspace_field(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(3)')

    #TODO: Dunno if I want to use properties for this nonsense.
    @property
    def name(self) -> str:
        return self.__name_field.text

    @property
    def keyspace(self) -> str:
        return self.__keyspace_field.text
   