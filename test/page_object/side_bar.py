"""Page object representing sidebar. Exports single class--the aforementioned page object."""

from __future__ import annotations
from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from page_object.common.page_object import PageObject
from page_object.add_job_page.add_job_page import AddJobPage
from page_object.library.dictionary import DictionaryManagement
from page_object.library.rules import RuleFileManagement
from page_object.library.charset import CharsetManagement
from page_object.library.mask import MaskManagement

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class SideBar(PageObject):
    """Represents the always present side bar in the Webadmin UI.
    Provides navigation methods to parts of the Webadmin UI.
    """

    def ensure_loaded(self):
        """Waits until the jobs button appears."""
        WebDriverWait(self.driver,30).until(lambda _:self.__jobs_button)

    @property
    def __jobs_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'nav-jobs-tab')
    @property
    def __library_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'nav-library-tab')
    @property
    def __system_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'nav-system-tab')
    @property
    def __add_job_button(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR,'a[href="/jobs/add"]')

    @property
    def __dictionary_library_button(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR,'a[href="/dictionaries"]')

    @property
    def __rule_file_library_button(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR,'a[href="/rules"]')

    @property
    def __charset_library_button(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR,'a[href="/charsets"]')

    @property
    def __mask_library_button(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR,'a[href="/masks"]')

    def goto_add_job(self) -> AddJobPage:
        """Opens the page Add Job page and returns an AddJobPage object.
        Previously generated objects by the `goto_XYZ` methods cease to be useable.
        """
        self.__jobs_button.click()
        self.__add_job_button.click()
        return AddJobPage(self.driver)
    
    def goto_dictionary_library(self) -> DictionaryManagement:
        """Opens the Dictionary page in the Library tab
        and returns a DictionaryManagement object.
        Previously generated objects by the `goto_XYZ` methods cease to be useable.
        """
        self.__library_button.click()
        self.__dictionary_library_button.click()
        return DictionaryManagement(self.driver)
    
    def goto_rule_file_library(self) -> RuleFileManagement:
        """Opens the Rules page in the Library tab
        and returns a RuleFileManagement object.
        Previously generated objects by the `goto_XYZ` methods cease to be useable.
        """
        self.__library_button.click()
        self.__rule_file_library_button.click()
        return RuleFileManagement(self.driver)

    def goto_charset_library(self) -> CharsetManagement:
        """Opens the Charsets page in the Library tab
        and returns a CharsetManagement object.
        Previously generated objects by the `goto_XYZ` methods cease to be useable.
        """
        self.__library_button.click()
        self.__charset_library_button.click()
        return CharsetManagement(self.driver)
    
    def goto_mask_library(self) -> MaskManagement:
        """Opens the Masks page in the Library tab
        and returns a MaskFileManagement object.
        Previously generated objects by the `goto_XYZ` methods cease to be useable.
        """
        self.__library_button.click()
        self.__mask_library_button.click()
        return MaskManagement(self.driver)
