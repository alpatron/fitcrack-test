from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement

from page_object.PageObject import PageObject

class DictionarySelection(PageObject):
    def __init__(self,driver:WebDriver,element:WebElement):
        super().__init__(driver)
        self.__element = element

    @property
    def __name_field(self) -> WebElement:
        return self.__element.find_element(By.CSS_SELECTOR,'td:nth-child(2) a')

    @property
    def __keyspace_field(self) -> WebElement:
        return self.__element.find_element(By.CSS_SELECTOR,'td:nth-child(3)')

    @property
    def __selection_checkbox(self) -> WebElement:
        return self.__element.find_element(By.CSS_SELECTOR, 'td:nth-child(1) i')


    #TODO: Dunno if I want to use properties for this nonsense.
    @property
    def name(self) -> str:
        return self.__name_field.text

    @property
    def keyspace(self) -> str:
        return self.__keyspace_field.text

    @property
    def selected(self) -> bool:
        checkboxClasses = self.__selection_checkbox.get_attribute('class')
        if 'mdi-checkbox-blank-outline' in checkboxClasses and not 'mdi-checkbox-marked' in checkboxClasses:
            return False
        elif 'mdi-checkbox-marked' in checkboxClasses and not 'mdi-checkbox-blank-outline' in checkboxClasses:
            return True
        else:
            raise Exception('The selection state of a checkbox could not be determined. This may indicate a brokem page object.')
    
    @selected.setter
    def selected(self,newState:bool) -> None:
        if newState == self.selected:
            return
        #We use the low-level API instead of regular element.click() because the way the app is coded
        #a ripple effect "obstructs" the checkbox, causing regular element.click() to fail saying the element's non-interactable.
        ActionChains(self.driver).click(self.__selection_checkbox).perform() 
   