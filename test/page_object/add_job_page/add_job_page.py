"""Page object representing Add Job page.
Exports single class--the aforementioned page object.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.relative_locator import locate_with

from page_object.common.page_object import PageObject
from page_object.add_job_page.input_settings import InputSettings
from page_object.add_job_page.attack_settings import AttackSettings
from page_object.job_detail_page import JobDetailPage
from page_object.common.helper import clear_workaround

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class AddJobPage(PageObject):
    """Represents the Add Job page that are always visible.
    The Add Job page is complex, so its sub-components are split into sub-page objects.
    This class contains methods that return those sub-page objects.
    """

    def ensure_loaded(self):
        """Waits until the job-name field appears."""
        WebDriverWait(self.driver,30).until(lambda _: self.__name_field)

    @property
    def __name_field(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'input').near({By.XPATH:'//label[text()="Name"]'})  # type: ignore
        )

    @property
    def __input_settings_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'job-step-1')

    @property
    def __attack_settings_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'job-step-2')

    @property
    def __host_assignment_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'job-step-3')

    @property
    def __additional_settings_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'job-step-4')

    @property
    def __create_button(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'button').near({By.XPATH:'//span[text()[contains(.,"Create")]]'})   # type: ignore
        )

    def set_job_name(self,name:str) -> None:
        """Sets the name of the job that is being created."""
        clear_workaround(self.__name_field)
        self.__name_field.send_keys(name)

    def get_job_name(self) -> str:
        """Returns the input name of the job that is being created."""
        return self.__name_field.get_attribute('value')

    def create_job(self) -> JobDetailPage:
        """Creates the job that is currently being set up.
        Upon creation, the page that shows the details of the created job is shown,
        so a JobDetailPage object is reutned. The current JobCreationObject ceases to be useable.
        """
        self.__create_button.click()
        return JobDetailPage(self.driver)

    def open_input_settings(self) -> InputSettings:
        """Opens the input settings and returns an InputSettings object representing
        these settings. The current JobCreationPage objects remains useable, but any
        previous objects created by the `open_XYZ_settings` methods using this object
        cease to be useable.
        """
        self.__input_settings_button.click()
        return InputSettings(self.driver)

    def open_attack_settings(self) -> AttackSettings:
        """Opens the attack settings and returns an AttackSettings object representing
        these settings. The current JobCreationPage objects remains useable, but any
        previous objects created by the `open_XYZ_settings` methods using this object
        cease to be useable.
        """
        self.__attack_settings_button.click()
        return AttackSettings(self.driver)
