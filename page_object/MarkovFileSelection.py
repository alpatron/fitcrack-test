from __future__ import annotations

from selenium.webdriver.common.by import By
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement

from page_object.GenericTableSelection import GenericTableSelection

class MarkovFileSelection(GenericTableSelection):
    '''
    This class represents a row from the markov-file-selection table on the brute-force attack settings on the Add Job page.
    '''
    @property
    def __name_field(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(2)')

    @property
    def __added_date(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(3)')

    #TODO: Dunno if I want to use properties for this nonsense.
    @property
    def name(self) -> str:
        return self.__name_field.text

    @property
    def added_date(self) -> str:
        return self.__added_date.text
   