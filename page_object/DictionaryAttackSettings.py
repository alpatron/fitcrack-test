from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support.relative_locator import locate_with
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement

from page_object.PageObject import PageObject
from page_object.DictionarySelection import DictionarySelection

class DictionaryAttackSettings(PageObject):
    def ensure_loaded(self):
        '''Waits until some dictionaries are available in the dictionary selection until a timeout.
        If the dictonary selector is still blank after the timeout, we assume that that is correct,
        and that there are indeed no dictionaries and proceed.
        Even if it succeeds and sees that dictionaries are loaded, we wait for five seconds to ensure
        that vuejs actually properly displays the elements.
        '''
        try:
            WebDriverWait(self.driver,30).until(lambda _: len(self.getAvailableDictionaries()) != 0)
            ActionChains(self.driver).pause(5).perform()
        except TimeoutError:
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
    
    def getAvailableDictionaries(self) -> List[DictionarySelection]:
        return [DictionarySelection(self.driver,tableRow) for tableRow in self.__dictionary_selection_table.find_elements(By.CSS_SELECTOR,'tbody tr')]
