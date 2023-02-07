from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException

from page_object.PageObject import PageObject
from page_object.DictionarySelection import DictionarySelection
from page_object.table_manipulation import activateElementsFromTableByListLookup, buildTableSelectionObjectsFromTable

from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class HybridAttackSettings(PageObject):
    def ensure_loaded(self) -> None:
        try:
            WebDriverWait(self.driver,30).until(lambda _: len(self.getAvailableDictionaries()) != 0)
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
            locate_with(By.TAG_NAME,'input').near({By.XPATH:'//label[text()="Enter mask"]'})  # type: ignore
        )

    def getAvailableDictionaries(self) -> List[DictionarySelection]:
        return buildTableSelectionObjectsFromTable(self.driver,self.__dictionary_selection_table,DictionarySelection)

    def selectDictionaries(self,wanted_dicts:List[str]) -> None:
        activateElementsFromTableByListLookup(self.getAvailableDictionaries(),lambda x: x.name,wanted_dicts)

    def setManglingRule(self,mangling_rule:str) -> None:
        self.__mangling_rule_input.clear()
        self.__mangling_rule_input.send_keys(mangling_rule)

    def setMask(self,mask:str) -> None:
        self.__mask_input.clear()
        self.__mask_input.send_keys(mask)