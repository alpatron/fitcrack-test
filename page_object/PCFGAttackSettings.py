from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains

from page_object.PageObject import PageObject
from page_object.RulefileSelection import RulefileSelection
from page_object.PCFGGrammarSelection import PCFGGrammarSelection
from page_object.table_manipulation import buildTableSelectionObjectsFromTable, activateElementsFromTableByListLookup
from page_object.helper import clearWorkaround

from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement

class PCFGAttackSettings(PageObject):
    def ensure_loaded(self) -> None:
        try:
            WebDriverWait(self.driver,30).until(lambda _: len(self.getAvailablePCFGGrammars()) != 0 and len(self.getAvailableRulefiles()) != 0)
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

    def getAvailablePCFGGrammars(self) -> List[PCFGGrammarSelection]:
        return buildTableSelectionObjectsFromTable(self.driver,self.__pcfg_grammar_selection_table,PCFGGrammarSelection)

    def selectPCFGGrammar(self,grammar:str) -> None:
        activateElementsFromTableByListLookup(self.getAvailablePCFGGrammars(),lambda x: x.name,[grammar])

    def getAvailableRulefiles(self) -> List[RulefileSelection]:
        return buildTableSelectionObjectsFromTable(self.driver,self.__rulefile_selection_table,RulefileSelection)
    
    def selectRulefiles(self,rulefiles:List[str]) -> None:
        activateElementsFromTableByListLookup(self.getAvailableRulefiles(),lambda x: x.name,rulefiles)
    
    def set_keyspace_limit(self,keyspace_limit:int) -> None:
        clearWorkaround(self.__keyspace_limit_input)
        self.__keyspace_limit_input.send_keys(str(keyspace_limit))

    