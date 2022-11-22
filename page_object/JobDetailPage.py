from __future__ import annotations

from selenium.webdriver.common.by import By

from typing import TYPE_CHECKING
from selenium.common.exceptions import JavascriptException, NoSuchElementException, TimeoutException
if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement

from page_object.PageObject import PageObject

class JobDetailPage(PageObject):
    
    @property
    def __start_button(self) -> WebElement:
        return self.driver.find_element(By.XPATH,'//span[text()[contains(.,"start")]]')