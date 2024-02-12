"""Page object representing PRINCE-attack settings in the Add Job page.
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
from page_object.table.dictionary_selection import DictionarySelection
from page_object.table.rule_file_selection import RuleFileSelection
from page_object.table.table_manipulation import build_table_row_objects_from_table, activate_elements_from_table_by_list_lookup, show_as_many_rows_per_table_page_as_possible
from page_object.common.helper import obstructed_click_workaround, get_checkbox_state, clear_workaround, click_away

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class PRINCEAttackSettings(PageObject):
    """This class represents the PRINCE-attack settings in the Add Job page."""

    def ensure_loaded(self) -> None:
        """Waits until dictionary and ruleset files are loaded, then waits for five more seconds
        for vuejs to settle and finish all animations and DOM manipulation.
        """
        try:
            WebDriverWait(self.driver,30).until(lambda _: len(self.get_available_dictionaries()) != 0 and len(self.get_available_rule_files()) != 0)
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

    @property
    def __password_duplicates_checkbox(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'input').to_left_of({By.XPATH:'//label[text()="Check for password duplicates"]'})  # type: ignore
        )

    @property
    def __case_permutation_checkbox(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'input').to_left_of({By.XPATH:'//label[text()="Case permutation"]'})  # type: ignore
        )

    @property
    def __minimal_password_length_input(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'input').below({By.XPATH:'//span[text()[contains(.,"Minimal length of passwords")]]'})  # type: ignore
        )

    @property
    def __maximal_password_length_input(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'input').below({By.XPATH:'//span[text()[contains(.,"Maximal length of passwords")]]'})  # type: ignore
        )

    @property
    def __minimal_number_of_elements_in_chain_input(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'input').below({By.XPATH:'//span[text()[contains(.,"Minimal number of elements per chain")]]'})  # type: ignore
        )

    @property
    def __maximal_number_of_elements_in_chain_input(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'input').below({By.XPATH:'//span[text()[contains(.,"Maximal number of elements per chain")]]'})  # type: ignore
        )

    @property
    def __keyspace_limit_input(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'input').below({By.XPATH:'//span[text()[contains(.,"Edit keyspace limit")]]'})  # type: ignore
        )

    @property
    def __random_rule_count_input(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.CSS_SELECTOR,'input[type="number"]').below({By.XPATH:'//span[text()[contains(.,"Generate random rules")]]'})  # type: ignore
        )

    def get_available_dictionaries(self) -> List[DictionarySelection]:
        """Returns a list of DictionarySelection objects representing the dictionary files
        that can be selected for the PRINCE attack.
        """
        click_away(self.driver)
        show_as_many_rows_per_table_page_as_possible(self.driver,self.__dictionary_selection_table)
        return build_table_row_objects_from_table(self.driver,self.__dictionary_selection_table,DictionarySelection)

    def select_dictionaries(self,wanted_dicts:List[str]) -> None:
        """Given a list of dictionary names (as they appear in the name column),
        selects the dictionaries with those names to be used in the PRINCE attack.
        Raises exception on failure.
        """
        activate_elements_from_table_by_list_lookup(self.get_available_dictionaries(),lambda x: x.name,wanted_dicts)

    def get_available_rule_files(self) -> List[RuleFileSelection]:
        """Returns a list of RuleFileSelection objects representing the rule files
        that can be selected for the dictionary attack.
        """
        click_away(self.driver)
        show_as_many_rows_per_table_page_as_possible(self.driver,self.__dictionary_selection_table)
        return build_table_row_objects_from_table(self.driver,self.__rule_file_selection_table,RuleFileSelection)

    def select_rule_file(self,wanted_rulefile:str) -> None:
        """Given the name of a rule (as it appears in the name column),
        selects the rule file with the given name to be used in the PRINCE attack.
        Raises exception on failure.
        """
        activate_elements_from_table_by_list_lookup(self.get_available_rule_files(),lambda x: x.name,[wanted_rulefile])

    def set_minimal_password_length(self,length:int) -> None:
        """Sets the minimal length of a potential password that can be generated by the attack."""
        clear_workaround(self.__minimal_password_length_input)
        self.__minimal_password_length_input.send_keys(str(length))

    def set_maximal_password_length(self,length:int) -> None:
        """Sets the maximal length of a potential password that can be generated by the attack."""
        clear_workaround(self.__maximal_password_length_input)
        self.__maximal_password_length_input.send_keys(str(length))

    def set_minimal_number_of_elements_per_chain(self,number:int) -> None:
        """Sets the minimal number of elements to be chained to generate a potential password."""
        clear_workaround(self.__minimal_number_of_elements_in_chain_input)
        self.__minimal_number_of_elements_in_chain_input.send_keys(str(number))

    def set_maximal_number_of_elements_per_chain(self,number:int) -> None:
        """Sets the maximal number of elements to be chained to generate a potential password."""
        clear_workaround(self.__maximal_number_of_elements_in_chain_input)
        self.__maximal_number_of_elements_in_chain_input.send_keys(str(number))

    def set_keyspace_limit(self, limit:int) -> None:
        """Sets the keyspace limit. Takes an int."""
        clear_workaround(self.__keyspace_limit_input)
        self.__keyspace_limit_input.send_keys(str(limit))

    def get_password_duplicate_check_state(self) -> bool:
        """Returns whether the password-duplicate check is turned on.
        Raises InvalidStateError if the state cannot be determined.
        """
        return get_checkbox_state(self.__password_duplicates_checkbox)

    def set_password_duplicate_check(self,new_state:bool) -> None:
        """Sets whether to check for duplicate password when generating them."""
        if new_state == self.get_password_duplicate_check_state():
            return
        obstructed_click_workaround(self.driver,self.__password_duplicates_checkbox)

    def get_case_permutation_state(self) -> bool:
        """Returns whether the case permutation is turned on.
        Raises InvalidStateError if the state cannot be determined.
        """
        return get_checkbox_state(self.__case_permutation_checkbox)

    def set_case_permutation_mode(self,new_state:bool) -> None:
        """Sets whether to use case permutation when generating passwords."""
        if new_state == self.get_case_permutation_state():
            return
        obstructed_click_workaround(self.driver,self.__case_permutation_checkbox)

    def set_random_rule_count(self,count:int) -> None:
        """Sets the number of random mangling rules to be used with the attack."""
        clear_workaround(self.__random_rule_count_input)
        self.__random_rule_count_input.send_keys(str(count))
