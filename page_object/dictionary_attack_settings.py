"""Page object representing dictionary-attack settings in the Add Job page.
Exports single class--the aforementioned page object.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, List

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support.relative_locator import locate_with
from selenium.common.exceptions import TimeoutException

from page_object.page_object import PageObject
from page_object.dictionary_selection import DictionarySelection
from page_object.rule_file_selection import RuleFileSelection
from page_object.table_manipulation import build_table_selection_objects_from_table, activate_elements_from_table_by_list_lookup

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class DictionaryAttackSettings(PageObject):
    """This class represents the dictionary-attack settings in the Add Job page."""

    def ensure_loaded(self):
        """Waits until some dictionaries are available in the dictionary selection until a timeout.
        If the dictionary selector is still blank after the timeout,
        we assume that that is correct, and that there are indeed no dictionaries and proceed.
        Even if it succeeds and sees that dictionaries are loaded, we wait for five seconds to
        ensure that vuejs actually properly displays the elements.
        """
        try:
            WebDriverWait(self.driver,30).until(lambda _: len(self.get_available_dictionaries()) != 0)
            ActionChains(self.driver).pause(5).perform()
        except TimeoutException:
            pass

    @property
    def __dictionary_selection_table(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'table').below({By.XPATH:'//span[text()[contains(.,"Select dictionary")]]'})  # type: ignore
        )

    @property
    def __rule_file_selection_table(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'table').below({By.XPATH:'//span[text()[contains(.,"Select rule file")]]'})  # type: ignore
        )

    def get_available_dictionaries(self) -> List[DictionarySelection]:
        """Returns a list of DictionarySelection objects representing the dictionaries
        that can be selected for the dictionary attack.
        """
        return build_table_selection_objects_from_table(self.driver,self.__dictionary_selection_table,DictionarySelection)

    def get_available_rule_files(self) -> List[RuleFileSelection]:
        """Returns a list of RuleFileSelection objects representing the rule files
        that can be selected for the dictionary attack.
        """
        return build_table_selection_objects_from_table(self.driver,self.__rule_file_selection_table,RuleFileSelection)

    def select_dictionaries(self,wanted_dicts:List[str]) -> None:
        """Given a list of dictionary names (as they appear in the name column),
        selects the dictionaries with those names to be used in the dictionary attack.
        Raises exception on failure.
        """
        activate_elements_from_table_by_list_lookup(self.get_available_dictionaries(),lambda x: x.name,wanted_dicts)

    def select_rule_files(self,wanted_rulefiles:List[str]) -> None:
        """Given a list of rule-file names (as they appear in the name column),
        selects the rule files with those names to be used in the dictionary attack.
        Raises exception on failure.
        """
        activate_elements_from_table_by_list_lookup(self.get_available_rule_files(),lambda x:x.name,wanted_rulefiles)
