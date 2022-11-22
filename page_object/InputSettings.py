from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import JavascriptException, NoSuchElementException
from selenium.webdriver.support.relative_locator import locate_with
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement

from page_object.PageObject import PageObject

class InputSettings(PageObject):
    @property
    def __manual_entry_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'job-input-mode-manual')
    @property
    def __hash_file_entry_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'job-input-mode-hashlist')
    @property
    def __file_extract_entry_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'job-input-mode-extract')

    @property
    def __hash_input_field(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR,'#hashes-input textarea')

    @property
    def __hash_type_selection_input(self) -> WebElement:
        return self.driver.find_element(By.ID,'hash-type-select')

    @property
    def __hash_type_selection_list(self) -> WebElement:
        return self.driver.find_element( #todo: replace back with near locator once Selenium accepts my PR
            locate_with(By.CLASS_NAME,'v-list').below(self.__hash_type_selection_input)  # type: ignore
        )

    def selectHashTypeExactly(self,hashtype:str) -> None: #Todo:this ain't really exact, but whateever; will be fixed later
        self.__hash_type_selection_input.click()
        self.__hash_type_selection_input.clear()
        self.__hash_type_selection_input.send_keys(hashtype)
        WebDriverWait(self.driver,30,ignored_exceptions={JavascriptException, NoSuchElementException}).until(lambda _: self.__hash_type_selection_list)
        self.__hash_type_selection_list.find_element(By.CSS_SELECTOR,'div:nth-child(1)').click()

    def getSelectedHashType(self) -> str:
        return self.__hash_input_field.get_attribute('value')

    def inputHashesManually(self,hashes:List[str]):
        self.__manual_entry_button.click()
        self.__hash_input_field.clear()
        self.__hash_input_field.send_keys('\n'.join(hashes))
