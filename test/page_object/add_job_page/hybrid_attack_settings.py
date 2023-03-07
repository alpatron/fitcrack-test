"""Page object representing hybrid-attack settings in the Add Job page.
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
from page_object.table.table_manipulation import activate_elements_from_table_by_list_lookup, build_table_row_objects_from_table, show_as_many_rows_per_table_page_as_possible
from page_object.common.helper import clear_workaround

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class HybridAttackSettings(PageObject):
    """This class represents the hybrid-attack settings in the Add Job page.
    This class is used for both types of hybrid attacks (mask first and wordlist first),
    and it's used in exactly the same way regardless of which kind of hybrid attack is used.    
    """

    def ensure_loaded(self) -> None:
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
    def __mangling_rule_input(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR,'[placeholder="Rule"]')

    @property
    def __mask_input(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'input').below({By.XPATH:'//span[text()[contains(.,"Type mask")]]'})  # type: ignore
        )

    def get_available_dictionaries(self) -> List[DictionarySelection]:
        """Returns a list of DictionarySelection objects representing the dictionaries
        that can be selected for the hybrid attack.
        """
        self._click_away()
        show_as_many_rows_per_table_page_as_possible(self.driver,self.__dictionary_selection_table)
        return build_table_row_objects_from_table(self.driver,self.__dictionary_selection_table,DictionarySelection)

    def select_dictionaries(self,wanted_dicts:List[str]) -> None:
        """Given a list of dictionary names (as they appear in the name column),
        selects the dictionaries with those names to be used in the hybrid attack.
        Raises exception on failure.
        """
        activate_elements_from_table_by_list_lookup(self.get_available_dictionaries(),lambda x: x.name,wanted_dicts)

    def set_mangling_rule(self,mangling_rule:str) -> None:
        """Sets the mangling rule to be used for the hybrid attack."""
        clear_workaround(self.__mangling_rule_input)
        self.__mangling_rule_input.send_keys(mangling_rule)

    def set_mask(self,mask:str) -> None:
        """Sets the mask to be used for the hybrid attack."""
        clear_workaround(self.__mask_input)
        self.__mask_input.send_keys(mask)
