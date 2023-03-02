from __future__ import annotations
from typing import TYPE_CHECKING, List, Union, overload

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.relative_locator import locate_with
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.expected_conditions import invisibility_of_element

from page_object.common.page_object import PageObject
from page_object.common.helper import get_checkbox_state
from page_object.common.exception import InvalidStateError
from page_object.table.dictionary_management_row import DictionaryManagementRow
from page_object.table.table_manipulation import build_table_row_objects_from_table

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement
    from pathlib import Path


class DictionaryManagement(PageObject):
    def ensure_loaded(self):
        WebDriverWait(self.driver,30,ignored_exceptions={InvalidStateError,NoSuchElementException}).until(lambda _: len(self.get_available_dictionaries()) != 0)

    @property
    def __dictionary_table(self) -> WebElement:
        return self.driver.find_element(By.TAG_NAME,'table')
    
    @property
    def __add_from_server_button(self) -> WebElement:
        return self.driver.find_element(By.XPATH,'//span[text()[contains(.,"Add from server")]]')
    
    @property
    def __upload_new_button(self) -> WebElement:
        return self.driver.find_element(By.XPATH,'//span[text()[contains(.,"Upload new")]]')

    @property
    def __sort_on_upload_checkbox(self) -> WebElement:
        label = self.driver.find_element(By.XPATH,'//label[text()="Sort on upload"]')
        input_id = label.get_attribute('for')
        return self.driver.find_element(By.ID,input_id)

    @property
    def __hex_dictionary_checkbox(self) -> WebElement:
        label = self.driver.find_element(By.XPATH,'//label[text()="HEX dictionary"]')
        input_id = label.get_attribute('for')
        return self.driver.find_element(By.ID,input_id)
    
    @property
    def __new_dictionary_file_input(self) -> WebElement:
        label = self.driver.find_element(By.XPATH,'//label[text()="Select files"]')
        input_id = label.get_attribute('for')
        return self.driver.find_element(By.ID,input_id)
    
    @property
    def __new_dictionary_upload_button(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'button').below(self.__new_dictionary_file_input) # type: ignore
        )
    
    def get_available_dictionaries(self) -> List[DictionaryManagementRow]:
        td_elements_in_table = self.__dictionary_table.find_elements(By.TAG_NAME,'td')
        if len(td_elements_in_table) == 1:
            if td_elements_in_table[0].text == 'No data available':
                return []
            try:
                if td_elements_in_table[0].text == 'Loading items...':
                    raise InvalidStateError('Dictionaries have not loaded yet.')
            except StaleElementReferenceException:
                return self.get_available_dictionaries()

        return build_table_row_objects_from_table(self.driver,self.__dictionary_table,DictionaryManagementRow)

    def dictionary_with_name_exists(self,name:str):
        for dictionary in self.get_available_dictionaries():
            if dictionary.name == name:
                return True
        return False

    def get_dictionary_with_name(self,name:str) -> DictionaryManagementRow:
        for dictionary in self.get_available_dictionaries():
            if dictionary.name == name:
                return dictionary
        raise InvalidStateError(f'Dictionary with name {name} could not be found.')

    def upload_dictionary(self,filename:Union[str,Path],sort_on_upload=False,hex_dictionary=False) -> None:
        if sort_on_upload != get_checkbox_state(self.__sort_on_upload_checkbox):
            self.__sort_on_upload_checkbox.click()
        if hex_dictionary != get_checkbox_state(self.__hex_dictionary_checkbox):
            self.__sort_on_upload_checkbox.click()
        self.__upload_new_button.click()
        WebDriverWait(self.driver,15).until(lambda _: self.__new_dictionary_file_input.is_displayed)
        #self.__new_dictionary_file_input.clear()
        self.__new_dictionary_file_input.send_keys(str(filename))
        self.__new_dictionary_upload_button.click()
        element = self.__new_dictionary_file_input
        WebDriverWait(self.driver,15).until(invisibility_of_element(element))
    