from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains

from page_object.PageObject import PageObject
from page_object.DictionarySelection import DictionarySelection
from page_object.RulefileSelection import RulefileSelection
from page_object.table_manipulation import buildTableSelectionObjectsFromTable, activateElementsFromTableByListLookup
from page_object.helper import obstructedClickWorkaround, getCheckboxState, clearWorkaround

from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement

class PrinceAttackSettings(PageObject):
    def ensure_loaded(self) -> None:
        try:
            WebDriverWait(self.driver,30).until(lambda _: len(self.getAvailableDictionaries()) != 0 and len(self.getAvailableRulefiles()) != 0)
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

    def getAvailableDictionaries(self) -> List[DictionarySelection]:
        return buildTableSelectionObjectsFromTable(self.driver,self.__dictionary_selection_table,DictionarySelection)

    def selectDictionaries(self,wanted_dicts:List[str]) -> None:
        activateElementsFromTableByListLookup(self.getAvailableDictionaries(),lambda x: x.name,wanted_dicts)
    
    def getAvailableRulefiles(self) -> List[RulefileSelection]:
        return buildTableSelectionObjectsFromTable(self.driver,self.__rule_file_selection_table,RulefileSelection)

    def selectRulefiles(self,wanted_rulefiles:List[str]) -> None:
        activateElementsFromTableByListLookup(self.getAvailableRulefiles(),lambda x: x.name,wanted_rulefiles)

    def setMinimalPasswordLenght(self,length:int) -> None:
        clearWorkaround(self.__minimal_password_length_input)
        self.__minimal_password_length_input.send_keys(str(length))

    def setMaximalPasswordLenght(self,length:int) -> None:
        clearWorkaround(self.__maximal_password_length_input)
        self.__maximal_password_length_input.send_keys(str(length))

    def setMinimalNumberOfElementsPerChain(self,number:int) -> None:
        clearWorkaround(self.__minimal_number_of_elements_in_chain_input)
        self.__minimal_number_of_elements_in_chain_input.send_keys(str(number))
    
    def setMaximalNumberOfElementsPerChain(self,number:int) -> None:
        clearWorkaround(self.__maximal_number_of_elements_in_chain_input)
        self.__maximal_number_of_elements_in_chain_input.send_keys(str(number))

    def setKeyspaceLimit(self, limit:int) -> None:
        clearWorkaround(self.__keyspace_limit_input)
        self.__keyspace_limit_input.send_keys(str(limit))

    def getPasswordDuplicateCheckState(self) -> bool:
        return getCheckboxState(self.__password_duplicates_checkbox)

    def setPasswordDuplicateCheck(self,newState:bool) -> None:
        if newState == self.getPasswordDuplicateCheckState():
            return
        obstructedClickWorkaround(self.driver,self.__password_duplicates_checkbox)

    def getCasePermutationState(self) -> bool:
        return getCheckboxState(self.__case_permutation_checkbox)

    def setCasePermutationMode(self,newState:bool) -> None:
        if newState == self.getCasePermutationState():
            return
        obstructedClickWorkaround(self.driver,self.__case_permutation_checkbox)

    def setRandomRuleCount(self,count:int) -> None:
        clearWorkaround(self.__random_rule_count_input)
        self.__random_rule_count_input.send_keys(str(count))
    
    