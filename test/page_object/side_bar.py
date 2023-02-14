"""Page object representing sidebar. Exports single class--the aforementioned page object."""

from __future__ import annotations
from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from page_object.page_object import PageObject
from page_object.add_job_page import AddJobPage

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

    def goto_add_job(self) -> AddJobPage:
        """Opens the page Add Job page and returns an AddJobPage object.
        Previously generated objects by the `goto_XYZ` methods cease to be useable.
        """
        self.__jobs_button.click()
        self.__add_job_button.click()
        return AddJobPage(self.driver)
