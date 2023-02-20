"""Page object representing the dashboard of Webadmin.
Exports single class--the aforementioned page object.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By

from page_object.common.page_object import PageObject

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class Dashboard(PageObject):
    """Represents the dashboard that is shown upon log in to Webadmin."""
    @property
    def __welcome_text(self) -> WebElement:
        return self.driver.find_element(By.TAG_NAME,'h1')
