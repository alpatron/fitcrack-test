"""Page object representing input settings in the Add Job page.
Exports single class--the aforementioned page object.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, List

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import JavascriptException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.relative_locator import locate_with

from page_object.common.page_object import PageObject
from page_object.common.helper import clear_workaround, click_away

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class InputSettings(PageObject):
    """Represents the Input Settings (step 1) on the Add Job page in Webadmin."""

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

    def _click_away(self):
        self.driver.find_element(By.ID,'job-step-1').click()

    def select_hash_type_exactly(self,hashtype:str) -> None: #Todo:this ain't really exact, but whateever; will be fixed later
        """Selects the hashtype that best matches the given `hashtype` string.
        Works by inputing the string into the hashtype-selection input and picking the first
        found option in the dropdown.
        """
        self.__hash_type_selection_input.click()
        clear_workaround(self.__hash_type_selection_input)
        self.__hash_type_selection_input.send_keys(hashtype)
        WebDriverWait(self.driver,30,ignored_exceptions={JavascriptException, NoSuchElementException}).until(lambda _: self.__hash_type_selection_list.is_displayed)
        ActionChains(self.driver).pause(2).perform() # Wait for 2 seconds to make sure vuejs animation is over
        self.__hash_type_selection_list.find_element(By.CSS_SELECTOR,'div:nth-child(1)').click()
        click_away(self.driver)

    def get_selected_hash_type(self) -> str:
        """Return the hash type that has been selected, as shown in the hash-type selector."""
        return self.__hash_input_field.get_attribute('value')

    def input_hashes_manually(self,hashes:List[str]):
        """Given a list of hashes, sets these as the attack input. Clears already input hashes."""
        self.__manual_entry_button.click()
        clear_workaround(self.__hash_input_field)
        self.__hash_input_field.send_keys('\n'.join(hashes))
