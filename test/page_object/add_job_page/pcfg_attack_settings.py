"""Page object representing PCFG-attack settings in the Add Job page.
Exports single class--the aforementioned page object.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, List

from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains

from page_object.common.page_object import PageObject
from page_object.table.rule_file_selection import RuleFileSelection
from page_object.table.pcfg_grammar_selection import PCFGGrammarSelection
from page_object.table.table_manipulation import build_table_row_objects_from_table, activate_elements_from_table_by_list_lookup, show_as_many_rows_per_table_page_as_possible
from page_object.common.helper import clear_workaround

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class PCFGAttackSettings(PageObject):
    """This class represents the PCFG-attack settings in the Add Job page."""

    def ensure_loaded(self) -> None:
        """Waits until PCFG-grammar and ruleset files are loaded, then waits for five more seconds
        for vuejs to settle and finish all animations and DOM manipulation.
        """
        try:
            WebDriverWait(self.driver,30).until(lambda _: len(self.get_available_pcfg_grammars()) != 0 and len(self.get_available_rule_files()) != 0)
            ActionChains(self.driver).pause(5).perform()
        except TimeoutException:
            pass

    @property
    def __pcfg_grammar_selection_table(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'table').below({By.XPATH:'//span[text()[contains(.,"Select PCFG grammar")]]'})  # type: ignore
        )

    @property
    def __rulefile_selection_table(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'table').below({By.XPATH:'//span[text()[contains(.,"Select rule file")]]'})  # type: ignore
        )

    @property
    def __keyspace_limit_input(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'input').below({By.XPATH:'//span[text()[contains(.,"Edit keyspace limit")]]'})  # type: ignore
        )

    def get_available_pcfg_grammars(self) -> List[PCFGGrammarSelection]:
        """Returns a list of PCFGGrammarSelection objects representing the grammar files
        that can be selected for the PCFG attack.
        """
        self._click_away()
        show_as_many_rows_per_table_page_as_possible(self.driver,self.__pcfg_grammar_selection_table)
        return build_table_row_objects_from_table(self.driver,self.__pcfg_grammar_selection_table,PCFGGrammarSelection)

    def select_pcfg_grammar(self,grammar:str) -> None:
        """Given the name of a PCFG-grammar file, selects this file to be used.
        Raises exception on failure.
        """
        activate_elements_from_table_by_list_lookup(self.get_available_pcfg_grammars(),lambda x: x.name,[grammar])

    def get_available_rule_files(self) -> List[RuleFileSelection]:
        """Returns a list of RuleFileSelection objects representing the rule files
        that can be selected for the PCFG attack.
        """
        self._click_away()
        show_as_many_rows_per_table_page_as_possible(self.driver,self.__rulefile_selection_table)
        return build_table_row_objects_from_table(self.driver,self.__rulefile_selection_table,RuleFileSelection)

    def select_rule_files(self,rulefiles:List[str]) -> None:
        """Given a list of rule-file names (as they appear in the name column),
        selects the rule files with those names to be used in the PCFG attack.
        Raises exception on failure.
        """
        activate_elements_from_table_by_list_lookup(self.get_available_rule_files(),lambda x: x.name,rulefiles)

    def set_keyspace_limit(self,keyspace_limit:int) -> None:
        """Sets the keyspace limit. Takes an int."""
        clear_workaround(self.__keyspace_limit_input)
        self.__keyspace_limit_input.send_keys(str(keyspace_limit))
