from __future__ import annotations
from typing import TYPE_CHECKING, List, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.relative_locator import locate_with
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

from page_object.common.page_object import PageObject
from page_object.common.exception import InvalidStateError
from page_object.table.charset_management_row import CharsetManagementRow
from page_object.table.table_manipulation import load_table_elements

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement
    from pathlib import Path


class CharsetManagement(PageObject):
    def ensure_loaded(self):
        WebDriverWait(self.driver,30,ignored_exceptions={InvalidStateError,NoSuchElementException}).until(
            lambda driver: 
                driver.find_element(By.XPATH,'//*[contains(@class, "v-card__title") and text()[contains(.,"Charsets")]]')
                and len(self.get_available_charset_files()) != 0
        )

    @property
    def __charset_file_table(self) -> WebElement:
        return self.driver.find_element(By.TAG_NAME,'table')
    
    @property
    def __upload_form(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'form').below(self.__charset_file_table) #type: ignore
        )
    
    @property
    def __upload_button(self) -> WebElement:
        return self.__upload_form.find_element(By.CSS_SELECTOR,'button.primary--text')
    
    @property
    def __file_input(self) -> WebElement:
        return self.__upload_form.find_element(By.TAG_NAME,'input')
    
    def get_available_charset_files(self) -> List[CharsetManagementRow]:
        return load_table_elements(self.driver,self.__charset_file_table,CharsetManagementRow)
    
    def get_charset_with_name(self,name:str) -> CharsetManagementRow:
        for charset_file in self.get_available_charset_files():
            if charset_file.name == name:
                return charset_file
        raise InvalidStateError(f'Charset file with name {name} could not be found.')

    def upload_charset(self,filename:Union[str,Path]) -> None:
        self.__file_input.send_keys(str(filename))
        self.__upload_button.click()
        self.get_snackbar_notification(raise_exception_on_error=True)
        self._wait_until_snackbar_notification_disappears()
    