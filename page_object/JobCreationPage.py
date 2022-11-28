from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import JavascriptException, NoSuchElementException
from selenium.webdriver.support.relative_locator import locate_with
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement

from page_object.PageObject import PageObject
from page_object.InputSettings import InputSettings
from page_object.AttackSettings import AttackSettings
from page_object.JobDetailPage import JobDetailPage

class JobCreationPage(PageObject):
    def ensure_loaded(self):
        WebDriverWait(self.driver,30,ignored_exceptions={JavascriptException, NoSuchElementException}).until(lambda _: self.__name_field)
    
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
    
    def setJobName(self,name:str) -> None:
        self.__name_field.clear()
        self.__name_field.send_keys(name)

    def getJobName(self) -> str:
        return self.__name_field.get_attribute('value')

    def createJob(self) -> JobDetailPage:
        self.__create_button.click()
        return JobDetailPage(self.driver)

    def openInputSettings(self) -> InputSettings:
        self.__input_settings_button.click()
        return InputSettings(self.driver)

    def openAttackSettings(self) -> AttackSettings:
        self.__attack_settings_button.click()
        return AttackSettings(self.driver)
