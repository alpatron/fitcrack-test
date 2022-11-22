from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver

class PageObject:
    def __init__(self,driver:WebDriver,no_ensure_loaded=False):
        self.driver = driver
        if not no_ensure_loaded:
            self.ensure_loaded()

    def ensure_loaded(self):
        pass