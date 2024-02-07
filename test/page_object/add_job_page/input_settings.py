"""Page object representing input settings in the Add Job page.
Exports single class--the aforementioned page object.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By

from page_object.common.page_object import PageObject
from page_object.library.add_hashlist import AddHashList

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class InputSettings(PageObject):
    """Represents the Input Settings (step 1) on the Add Job page in Webadmin."""

    @property
    def __new_hash_list_button(self) -> WebElement:
        return self.driver.find_element(By.XPATH,'//span[text()[contains(.," Create new input hashlist ")]]')
    
    def goto_attach_new_hash_list(self) -> AddHashList:
        from page_object.add_job_page.add_job_page import AddJobPage
        self.__new_hash_list_button.click()
        return AddHashList(self.driver,AddJobPage(self.driver,no_ensure_loaded=True))
