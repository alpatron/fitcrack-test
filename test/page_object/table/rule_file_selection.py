"""Page object representing a row in a rule-file-selection table.
Exports single class--the aforementioned page object.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By

from page_object.table.generic_table_selection import GenericTableSelection

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class RuleFileSelection(GenericTableSelection):
    """This class represents a row from the rulefile-selection tables on the Add Job page."""

    @property
    def __name_field(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(2) a')

    @property
    def __rule_count_field(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(3)')

    #TODO: Dunno if I want to use properties for this nonsense.
    @property
    def name(self) -> str:
        """The file name of the rule file."""
        return self.__name_field.text

    @property
    def rule_count(self) -> str:
        """The number of rules contained in the rule file."""
        return self.__rule_count_field.text
