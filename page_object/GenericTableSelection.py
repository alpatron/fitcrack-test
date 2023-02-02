from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement

from page_object.PageObject import PageObject

class GenericTableSelection(PageObject):
    '''
    This class represents a generic object representing a selectable table row.
    
    For example, one such table is the dictionary selector in the Dictionary Attack
    settings in the Add Job screen of Fitcrack. By itself, this class offers one function:
    the ability to query whether the a table row is selected (whether the checkbox is checked)
    and the ability to check/uncheck it.

    You should create a new class and inherit from this one to add methods to query
    more information about a selectable table row than just the checkbox.
    E.g. see the DictionarySelection class for a non-generic page object.
    '''
    
    def __init__(self,driver:WebDriver,element:WebElement):
        super().__init__(driver)
        self._element = element

    @property
    def __selection_checkbox(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR, 'td:nth-child(1) i')

    @property
    def selected(self) -> bool:
        checkboxClasses = self.__selection_checkbox.get_attribute('class')
        if 'mdi-checkbox-blank-outline' in checkboxClasses and not 'mdi-checkbox-marked' in checkboxClasses:
            return False
        elif 'mdi-checkbox-marked' in checkboxClasses and not 'mdi-checkbox-blank-outline' in checkboxClasses:
            return True
        else:
            raise Exception('The selection state of a checkbox could not be determined. This may indicate a broken page object.')
    
    @selected.setter
    def selected(self,newState:bool) -> None:
        if newState == self.selected:
            return
        #We use the low-level API instead of regular element.click() because the way the app is coded
        #a ripple effect "obstructs" the checkbox, causing regular element.click() to fail saying the element's non-interactable.
        _ = self.__selection_checkbox.screenshot_as_base64 #Workaround because the current version of Selenium has broken scroll support.
        ActionChains(self.driver).click(self.__selection_checkbox).perform() 
   