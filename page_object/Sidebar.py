from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement

from page_object.PageObject import PageObject
from page_object.JobCreationPage import JobCreationPage

class SideBar(PageObject):
    
    def ensure_loaded(self):
        WebDriverWait(self.driver,30).until(lambda _:self.jobs_button)
    
    @property
    def jobs_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'nav-jobs-tab')    
    @property
    def library_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'nav-library-tab')
    @property
    def system_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'nav-system-tab')
    @property
    def add_job_button(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR,'a[href="/jobs/add"]')

    def goto_create_job(self) -> JobCreationPage:
        self.jobs_button.click()
        self.add_job_button.click()
        return JobCreationPage(self.driver)
