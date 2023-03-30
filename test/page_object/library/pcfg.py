from __future__ import annotations
from typing import TYPE_CHECKING, List, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.relative_locator import locate_with
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains

from page_object.common.page_object import PageObject
from page_object.common.helper import click_away, predicate_in_list
from page_object.common.exception import InvalidStateError
from page_object.table.pcfg_management_row import PCFGManagementRow
from page_object.table.dictionary_selection import DictionarySelection
from page_object.table.table_manipulation import load_table_elements

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement
    from pathlib import Path


class PCFGManagement(PageObject):
    def ensure_loaded(self):
        WebDriverWait(self.driver,30,ignored_exceptions={InvalidStateError,NoSuchElementException}).until(
            lambda driver: 
                driver.find_element(By.XPATH,'//*[contains(@class, "v-card__title") and text()[contains(.,"PCFGs")]]')
                and len(self.get_available_pcfgs()) != 0
        )

    @property
    def __pcfg_file_table(self) -> WebElement:
        return self.driver.find_element(By.TAG_NAME,'table')
    
    @property
    def __add_new_button(self) -> WebElement:
        return self.driver.find_element(By.XPATH,'//span[text()[contains(.,"Add new")]]')
    
    @property
    def __upload_dialog_upload_file_mode_selector(self) -> WebElement:
        return self.driver.find_element(By.XPATH,'//div[text()[contains(.,"Upload file")]]')
    
    @property
    def __upload_dialog_from_dictionary_mode_selector(self) -> WebElement:
        return self.driver.find_element(By.XPATH,'//div[text()[contains(.,"Make from dictionary")]]')

    @property
    def __upload_dialog_from_dictionary_table(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR,'.v-dialog--active table')

    @property
    def __upload_dialog_from_dictionary_submit_button(self) -> WebElement:
        return self.driver.find_element(By.XPATH,'//span[text()[contains(.,"Make from dictionary")]]')

    @property
    def __upload_dialog_file_input(self) -> WebElement:
        label = self.driver.find_element(By.XPATH,'//label[text()="Select files"]')
        input_id = label.get_attribute('for')
        return self.driver.find_element(By.ID,input_id)
    
    @property
    def __upload_dialog_upload_button(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'button').below(self.__upload_dialog_file_input) # type: ignore
        )

    def get_available_pcfgs(self) -> List[PCFGManagementRow]:
        return load_table_elements(self.driver,self.__pcfg_file_table,PCFGManagementRow)

    def upload_pcfg(self,filename:Union[str,Path]) -> None:
        self.__add_new_button.click()
        ActionChains(self.driver).pause(4).perform() #Wait for animation to finish
        self.__upload_dialog_upload_file_mode_selector.click()
        self.__upload_dialog_file_input.send_keys(str(filename))
        self.__upload_dialog_upload_button.click()
        self.get_snackbar_notification(raise_exception_on_error=True)
        self._wait_until_snackbar_notification_disappears()
    
    def get_available_dictionaries(self) -> List[str]:
        self.__add_new_button.click()
        self.__upload_dialog_from_dictionary_mode_selector.click()
        dictionaries = load_table_elements(self.driver,self.__upload_dialog_from_dictionary_table,DictionarySelection,in_dialog=True)
        dictionary_names = [x.name for x in dictionaries]
        click_away(self.driver)
        return dictionary_names
    
    def make_pcfg_from_dictionary(self,dictionary_name:str):
        self.__add_new_button.click()
        ActionChains(self.driver).pause(4).perform() #Wait for animation to finish
        self.__upload_dialog_from_dictionary_mode_selector.click()
        dictionaries = load_table_elements(self.driver,self.__upload_dialog_from_dictionary_table,DictionarySelection,in_dialog=True)
        wanted_dictionary = predicate_in_list(lambda x: x.name == dictionary_name,dictionaries)
        wanted_dictionary.enabled = True
        self.__upload_dialog_from_dictionary_submit_button.click()
        self._wait_until_dialog_closes(300)
        self.get_snackbar_notification(raise_exception_on_error=True)
        self._wait_until_snackbar_notification_disappears()
    