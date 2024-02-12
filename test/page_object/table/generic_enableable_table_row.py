"""Module containing the base GenericEnableableTableRow class for dealing with Webadmin tables."""

from __future__ import annotations
from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By

from page_object.common.page_object import PageComponentObject
from page_object.common.helper import obstructed_click_workaround
from page_object.common.exception import InvalidStateError

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement


class GenericEnableableTableRow(PageComponentObject):
    """This class represents a generic object representing a table row that can be enabled;
    that is to say a table row that has a checkbox as the first element.
    
    For example, one such table is the dictionary selector in the Dictionary Attack
    settings in the Add Job screen of Fitcrack. By itself, this class offers two functions:
    the ability to query whether the a table row is enabled (whether the checkbox is checked)
    and the ability to check/uncheck it.

    You should create a new class and inherit from this one to add methods to query
    more information about a selectable table row than just the checkbox.
    E.g. see the DictionarySelection class for a non-generic page object.
    """

    @property
    def __selection_checkbox(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR, 'td:nth-child(1) i')

    @property
    def enabled(self) -> bool:
        """Whether a row in a table is enabled; i.e. whether its corresponding checkbox is checked.
        
        Do note that that this method does not use the `getCheckboxState` function from the
        `helper` file. This is because table rows in Webadmin use a different kind of checkbox than
        the regular ones, so a different kind of selection check needs to be used.
        
        Raises an InvalidStateError if the enabled state cannot be determined."""

        checkbox_classes = self.__selection_checkbox.get_attribute('class')
        if 'mdi-checkbox-blank-outline' in checkbox_classes and not 'mdi-checkbox-marked' in checkbox_classes: # type: ignore
            return False
        elif 'mdi-checkbox-marked' in checkbox_classes and not 'mdi-checkbox-blank-outline' in checkbox_classes: # type: ignore
            return True
        else:
            raise InvalidStateError(
                'The enable-ness state of a table-row checkbox could not be determined.'
                'This may indicate a broken page object.'
            )

    @enabled.setter
    def enabled(self,new_state:bool) -> None:
        if new_state == self.enabled:
            return
        obstructed_click_workaround(self.driver,self.__selection_checkbox)
