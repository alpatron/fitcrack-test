"""Page object representing combination-attack settings in the Add Job page.
Exports single class--the aforementioned page object.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, List

from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException

from page_object.common.page_object import PageObject
from page_object.table.dictionary_selection import DictionarySelection
from page_object.table.table_manipulation import build_table_row_objects_from_table, activate_elements_from_table_by_list_lookup, show_as_many_rows_per_table_page_as_possible
from page_object.common.helper import clear_workaround, click_away

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class CombinationAttackSettings(PageObject):
    """This class represents the combination-attack settings in the Add Job page."""

    def ensure_loaded(self):
        """Waits until some dictionaries are available in the dictionary selections until a timeout.
        If at least one dictionary selector is still blank after the timeout, we assume that that
        is correct, and that there are indeed no dictionaries and proceed.
        Even if it succeeds and sees that dictionaries are loaded, we wait for five second
        to ensure that vuejs actually properly displays the elements.
        """
        try:
            WebDriverWait(self.driver,30).until(lambda _: len(self.get_available_left_dictionaries()) != 0 and len(self.get_available_right_dictionaries()) != 0)
            ActionChains(self.driver).pause(5).perform()
        except TimeoutException:
            pass

    @property
    def __left_dictionary_selection_table(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'table').below({By.XPATH:'//span[text()[contains(.,"Select left dictionary")]]'})  # type: ignore
        )

    @property
    def __right_dictionary_selection_table(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'table').below({By.XPATH:'//span[text()[contains(.,"Select right dictionary")]]'})  # type: ignore
        )

    @property
    def __left_rule_input(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'input').below({By.XPATH:'//span[text()[contains(.,"Type left rule")]]'})  # type: ignore
        )

    @property
    def __right_rule_input(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'input').below({By.XPATH:'//span[text()[contains(.,"Type right rule")]]'})  # type: ignore
        )

    def get_available_left_dictionaries(self) -> List[DictionarySelection]:
        """Returns a list of DictionarySelection objects representing the dictionaries
        on the left side of the combination attack.
        """
        click_away(self.driver)
        show_as_many_rows_per_table_page_as_possible(self.driver,self.__left_dictionary_selection_table)
        return build_table_row_objects_from_table(self.driver,self.__left_dictionary_selection_table,DictionarySelection)

    def get_available_right_dictionaries(self) -> List[DictionarySelection]:
        """Returns a list of DictionarySelection objects representing the dictionaries
        on the right side of the combination attack.
        """
        click_away(self.driver)
        show_as_many_rows_per_table_page_as_possible(self.driver,self.__right_dictionary_selection_table)
        return build_table_row_objects_from_table(self.driver,self.__right_dictionary_selection_table,DictionarySelection)

    def select_left_dictionaries(self,wanted_dicts:List[str]) -> None:
        """Given a list of dictionary names (as they appear in the name column),
        selects the dictionaries with those names to be used on the left side of the
        combination attack. Raises exception on failure.
        """
        activate_elements_from_table_by_list_lookup(self.get_available_left_dictionaries(),lambda x: x.name,wanted_dicts)

    def select_right_dictionaries(self,wanted_dicts:List[str]) -> None:
        """Given a list of dictionary names (as they appear in the name column),
        selects the dictionaries with those names to be used on the right side of the
        combination attack. Raises exception on failure.
        """
        activate_elements_from_table_by_list_lookup(self.get_available_right_dictionaries(),lambda x: x.name,wanted_dicts)

    def set_left_mangling_rule(self,mangling_rule:str) -> None:
        """Sets the mangling rule to be used on the left side of the combination attack."""
        clear_workaround(self.__left_rule_input)
        self.__left_rule_input.send_keys(mangling_rule)

    def set_right_mangling_rule(self,mangling_rule:str) -> None:
        """Sets the mangling rule to be used on the right side of the combination attack."""
        clear_workaround(self.__right_rule_input)
        self.__right_rule_input.send_keys(mangling_rule)
