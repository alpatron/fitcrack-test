"""Module containing the base GenericTableSelection class for dealing with Webadmin tables."""

from __future__ import annotations
from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By

from page_object.page_object import PageObject
from page_object.helper import obstructed_click_workaround
from page_object.exception import InvalidStateError

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement


class GenericTableSelection(PageObject):
    """This class represents a generic object representing a selectable table row.
    
    For example, one such table is the dictionary selector in the Dictionary Attack
    settings in the Add Job screen of Fitcrack. By itself, this class offers two functions:
    the ability to query whether the a table row is selected (whether the checkbox is checked)
    and the ability to check/uncheck it.

    You should create a new class and inherit from this one to add methods to query
    more information about a selectable table row than just the checkbox.
    E.g. see the DictionarySelection class for a non-generic page object.
    """

    def __init__(self,driver:WebDriver,element:WebElement):
        super().__init__(driver)
        self._element = element

    @property
    def __selection_checkbox(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR, 'td:nth-child(1) i')

    @property
    def selected(self) -> bool:
        """Whether a row in a table is selected; i.e. whether its corresponding checkbox is checked.
        
        Do note that that this method does not use the `getCheckboxState` function from the
        `helper` file. This is because table rows in Webadmin use a different kind of checkbox than
        the regular ones, so a different kind of selection check needs to be used.
        
        Raises an InvalidStateError if the selected state cannot be determined."""
        
        checkbox_classes = self.__selection_checkbox.get_attribute('class')
        if 'mdi-checkbox-blank-outline' in checkbox_classes and not 'mdi-checkbox-marked' in checkbox_classes:
            return False
        elif 'mdi-checkbox-marked' in checkbox_classes and not 'mdi-checkbox-blank-outline' in checkbox_classes:
            return True
        else:
            raise InvalidStateError(
                'The selection state of a table-row checkbox could not be determined.'
                'This may indicate a broken page object.'
            )

    @selected.setter
    def selected(self,new_state:bool) -> None:
        if new_state == self.selected:
            return
        obstructed_click_workaround(self.driver,self.__selection_checkbox)
