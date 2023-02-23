from __future__ import annotations
from typing import TYPE_CHECKING, List

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import JavascriptException, NoSuchElementException
from selenium.webdriver.support.relative_locator import locate_with

from page_object.common.page_object import PageObject
from page_object.add_job_page.input_settings import InputSettings
from page_object.add_job_page.attack_settings import AttackSettings
from page_object.job_detail_page import JobDetailPage
from page_object.common.helper import clear_workaround, get_checkbox_state
from page_object.table.dictionary_management_row import DictionaryManagementRow
from page_object.table.table_manipulation import build_table_row_objects_from_table

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class AddJobPage(PageObject):
    def ensure_loaded(self):
        pass

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
        return build_table_row_objects_from_table(self.driver,self.__dictionary_table,DictionaryManagementRow)
    
    def upload_dictionary(self,filename:str,sort_on_upload=False,hex_dictionary=False) -> None:
        if sort_on_upload != get_checkbox_state(self.__sort_on_upload_checkbox):
            self.__sort_on_upload_checkbox.click()
        if hex_dictionary != get_checkbox_state(self.__hex_dictionary_checkbox):
            self.__sort_on_upload_checkbox.click()
        self.__upload_new_button.click()
        self.__new_dictionary_file_input.clear()
        self.__new_dictionary_file_input.send_keys(filename)
        self.__new_dictionary_upload_button.click()


