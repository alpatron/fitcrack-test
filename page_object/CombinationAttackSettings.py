from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException

from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement

from page_object.PageObject import PageObject
from page_object.DictionarySelection import DictionarySelection
from page_object.table_manipulation import buildTableSelectionObjectsFromTable, activateElementsFromTableByListLookup

class CombinationAttackSettings(PageObject):
    def ensure_loaded(self):
        '''Waits until some dictionaries are available in the dictionary selection until a timeout.
        If the dictionary selector is still blank after the timeout, we assume that that is correct,
        and that there are indeed no dictionaries and proceed.
        Even if it succeeds and sees that dictionaries are loaded, we wait for five seconds to ensure
        that vuejs actually properly displays the elements.
        '''
        try:
            WebDriverWait(self.driver,30).until(lambda _: len(self.getAvailableLeftDictionaries()) != 0 and (self.getAvailableRightDictionaries()) != 0)
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

    def getAvailableLeftDictionaries(self) -> List[DictionarySelection]:
        return buildTableSelectionObjectsFromTable(self.driver,self.__left_dictionary_selection_table,DictionarySelection)

    def getAvailableRightDictionaries(self) -> List[DictionarySelection]:
        return buildTableSelectionObjectsFromTable(self.driver,self.__right_dictionary_selection_table,DictionarySelection)

    def selectLeftDictionaries(self,wanted_dicts:List[str]) -> None:
        activateElementsFromTableByListLookup(self.getAvailableLeftDictionaries(),lambda x: x.name,wanted_dicts)

    def selectRightDictionaries(self,wanted_dicts:List[str]) -> None:
        activateElementsFromTableByListLookup(self.getAvailableRightDictionaries(),lambda x: x.name,wanted_dicts)

    def setLeftManglingRule(self,mangling_rule:str) -> None:
        self.__left_rule_input.clear()
        self.__left_rule_input.send_keys(mangling_rule)

    def setRightManglingRule(self,mangling_rule:str) -> None:
        self.__right_rule_input.clear()
        self.__right_rule_input.send_keys(mangling_rule)




    
