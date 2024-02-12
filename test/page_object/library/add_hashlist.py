"""Page object representing input settings in the Add Job page.
Exports single class--the aforementioned page object.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, List, Union, Optional
from enum import Enum

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import JavascriptException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.relative_locator import locate_with

from page_object.common.page_object import PageObject
from page_object.common.helper import clear_workaround, click_away, get_checkbox_state, obstructed_click_workaround


if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement
    from pathlib import Path


class ValidationMode(Enum):
    """Enum describing the possible validation modes that can be used
    when adding hashes to hash lists.
    """
    STRICT = 'fail_invalid'
    SKIPPING = 'skip_invalid'
    NO_VALIDATE = 'no_validate'


class AddHashList(PageObject):
    """Represents the screen for creating hash lists."""

    def __init__(self,driver:WebDriver,home_page_object:PageObject,no_ensure_loaded=False):
        super().__init__(driver,no_ensure_loaded)
        self.home_page_object = home_page_object

    def ensure_loaded(self):
        WebDriverWait(self.driver,30,ignored_exceptions={JavascriptException, NoSuchElementException}).until(lambda _: self.__manual_entry_button and self.__confirm_button)

    @property
    def __manual_entry_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'input-manual')
    @property
    def __hash_file_entry_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'input-file')
    @property
    def __file_extract_entry_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'input-extract')

    @property
    def __validation_mode_strict_button(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR,'button[value="fail_invalid"]')

    @property
    def __validation_mode_skipping_button(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR,'button[value="skip_invalid"]')

    @property
    def __validation_mode_none_button(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR,'button[value="no_validate"]')

    @property
    def __hash_input_field(self) -> WebElement:
        return self.driver.find_element(By.TAG_NAME,'textarea')

    @property
    def __hash_type_selection_input(self) -> WebElement:
        label = self.driver.find_element(By.XPATH,'//label[text()="Select hash type"]')
        input_id = label.get_attribute('for')
        return self.driver.find_element(By.ID,input_id)

    @property
    def __hash_type_selection_list(self) -> WebElement:
        return self.driver.find_element( #todo: replace back with near locator once Selenium accepts my PR
            locate_with(By.CLASS_NAME,'v-list').below(self.__hash_type_selection_input)  # type: ignore
        )

    @property
    def __hash_file_input(self) -> WebElement:
        label = self.driver.find_element(By.XPATH,'//label[text()="Select hashlist file to add"]')
        input_id = label.get_attribute('for')
        return self.driver.find_element(By.ID,input_id)

    @property
    def __encrypted_file_input(self) -> WebElement:
        label = self.driver.find_element(By.XPATH,'//label[text()="Select protected file to extract"]')
        input_id = label.get_attribute('for')
        return self.driver.find_element(By.ID,input_id)

    @property
    def __cancel_button(self) -> WebElement:
        return self.driver.find_element(By.XPATH,'//span[text()[contains(.,"Cancel")]]')

    @property
    def __confirm_button(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'span').to_right_of(self.__cancel_button) # type: ignore
        )

    @property
    def __binary_hash_file_checkbox(self) -> WebElement:
        label = self.driver.find_element(By.XPATH,'//label[text()="Treat as a binary hashlist file"]')
        input_id = label.get_attribute('for')
        return self.driver.find_element(By.ID,input_id)

    @property
    def __hash_list_name_input(self) -> WebElement:
        label = self.driver.find_element(By.XPATH,'//label[text()="Name"]')
        input_id = label.get_attribute('for')
        return self.driver.find_element(By.ID,input_id)

    def select_hash_type_exactly(self,hashtype:str) -> None:
        """Selects the hashtype that best matches the given `hashtype` string.
        Works by inputting the string into the hashtype-selection input and picking the first
        found option in the dropdown.
        """
        self.__hash_type_selection_input.click()
        clear_workaround(self.__hash_type_selection_input)
        self.__hash_type_selection_input.send_keys(hashtype)
        WebDriverWait(self.driver,30,ignored_exceptions={JavascriptException, NoSuchElementException}).until(lambda _: self.__hash_type_selection_list.is_displayed)
        ActionChains(self.driver).pause(2).perform() # Wait for 4 seconds to ensure vuejs animation is over
        WebDriverWait(self.driver,30,ignored_exceptions={JavascriptException, NoSuchElementException}).until(lambda _: len(self.__hash_type_selection_list.text) > 100) # Wait until some hash types actually get loaded
        self.__hash_type_selection_list.find_element(By.CSS_SELECTOR,'div:nth-child(1)').click()
        click_away(self.driver)

    def select_hash_validation_mode(self,validation_mode:ValidationMode) -> None:
        match validation_mode:
            case ValidationMode.STRICT:
                self.__validation_mode_strict_button.click()
            case ValidationMode.SKIPPING:
                self.__validation_mode_skipping_button.click()
            case ValidationMode.NO_VALIDATE:
                self.__validation_mode_none_button.click()

    def __workaround_hash_input_send_keys(self,hashes:List[str]) -> None:
        escaped_new_line = '\\n'
        self.driver.execute_script(f'document.querySelector("textarea").value = "{escaped_new_line.join(hashes)}"')
        self.__hash_input_field.send_keys(' ')
        self.__hash_input_field.send_keys(Keys.BACKSPACE)

    def input_hashes_manually(self,hashes:List[str],hashtype:str,validation_mode=ValidationMode.STRICT,hash_list_name:Optional[str]=None):
        """Given a list of hashes, creates a hash list with the given hashes."""
        self.__manual_entry_button.click()
        if hash_list_name is not None:
            clear_workaround(self.__hash_list_name_input)
            self.__hash_list_name_input.send_keys(hash_list_name)
        self.select_hash_type_exactly(hashtype)
        self.select_hash_validation_mode(validation_mode)
        clear_workaround(self.__hash_input_field)
        self.__workaround_hash_input_send_keys(hashes)
        self.__confirm_button.click()
        self.home_page_object.ensure_loaded()

    def input_hashes_from_hash_file(self,filename:Union[str,Path],hashtype:str,binary_hash_file=False,validation_mode=ValidationMode.STRICT,hash_list_name:Optional[str]=None) -> None:
        """Given a path to a hash file, sets it as the attack input."""
        self.__hash_file_entry_button.click()
        if hash_list_name is not None:
            clear_workaround(self.__hash_list_name_input)
            self.__hash_list_name_input.send_keys(hash_list_name)
        self.select_hash_type_exactly(hashtype)
        self.select_hash_validation_mode(validation_mode)
        if get_checkbox_state(self.__binary_hash_file_checkbox) != binary_hash_file:
            obstructed_click_workaround(self.driver,self.__binary_hash_file_checkbox)
        self.__hash_file_input.send_keys(str(filename))
        self.__confirm_button.click()
        self.home_page_object.ensure_loaded()

    def extract_hash_from_file(self,filename:Union[str,Path],hash_list_name:Optional[str]=None) -> None:
        """Given a path to an encrypted file, extracts the hash from it and sets it as the input."""
        self.__file_extract_entry_button.click()
        if hash_list_name is not None:
            clear_workaround(self.__hash_list_name_input)
            self.__hash_list_name_input.send_keys(hash_list_name)
        self.__encrypted_file_input.send_keys(str(filename))
        self.__confirm_button.click()
        self.home_page_object.ensure_loaded()
