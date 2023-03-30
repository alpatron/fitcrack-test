from __future__ import annotations
from typing import TYPE_CHECKING, List, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.relative_locator import locate_with
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException

from page_object.common.page_object import PageObject
from page_object.common.helper import click_away
from page_object.common.exception import InvalidStateError
from page_object.table.rule_file_management_row import RuleFileManagementRow
from page_object.table.table_manipulation import build_table_row_objects_from_table, show_as_many_rows_per_table_page_as_possible

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement
    from pathlib import Path


class RuleFileManagement(PageObject):
    def ensure_loaded(self):
        WebDriverWait(self.driver,30,ignored_exceptions={InvalidStateError,NoSuchElementException,ElementClickInterceptedException}).until(
            lambda driver: 
                driver.find_element(By.XPATH,'//*[contains(@class, "v-card__title") and text()[contains(.,"Rules")]]')
                and len(self.get_available_rule_files()) != 0
        )

    @property
    def __rule_file_table(self) -> WebElement:
        return self.driver.find_element(By.TAG_NAME,'table')
    
    @property
    def __upload_form(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'form').below(self.__rule_file_table) #type: ignore
        )
    
    @property
    def __upload_button(self) -> WebElement:
        return self.__upload_form.find_element(By.CSS_SELECTOR,'button.primary--text')
    
    @property
    def __file_input(self) -> WebElement:
        return self.__upload_form.find_element(By.TAG_NAME,'input')
    
    def get_available_rule_files(self) -> List[RuleFileManagementRow]:
        click_away(self.driver)
        show_as_many_rows_per_table_page_as_possible(self.driver,self.__rule_file_table)

        td_elements_in_table = self.__rule_file_table.find_elements(By.TAG_NAME,'td')
        if len(td_elements_in_table) == 1:
            try:
                if td_elements_in_table[0].text == 'No data available':
                    return []
                if td_elements_in_table[0].text == 'Loading items...':
                    raise InvalidStateError('Rule files have not loaded yet.')
            except StaleElementReferenceException:
                return self.get_available_rule_files()

        return build_table_row_objects_from_table(self.driver,self.__rule_file_table,RuleFileManagementRow)

    def rule_file_with_name_exists(self,name:str):
        for rule_file in self.get_available_rule_files():
            if rule_file.name == name:
                return True
        return False
    
    def get_rule_file_with_name(self,name:str) -> RuleFileManagementRow:
        for rule_file in self.get_available_rule_files():
            if rule_file.name == name:
                return rule_file
        raise InvalidStateError(f'Rule file with name {name} could not be found.')

    def upload_rule_file(self,filename:Union[str,Path]) -> None:
        self.__file_input.send_keys(str(filename))
        self.__upload_button.click()
        self.get_snackbar_notification(raise_exception_on_error=True)
        self._wait_until_snackbar_notification_disappears()
    