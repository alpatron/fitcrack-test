from __future__ import annotations

from selenium.webdriver.common.by import By

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement

from page_object.PageObject import PageObject

class Dashboard(PageObject):
    @property
    def welcome_text(self) -> WebElement:
        return self.driver.find_element(By.TAG_NAME,'h1')