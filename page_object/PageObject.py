from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver

class PageObject:
    def __init__(self,driver:WebDriver,no_ensure_loaded=False):
        self.driver = driver
        if not no_ensure_loaded:
            self.ensure_loaded()

    def ensure_loaded(self) -> None:
        pass
    
    def _click_away(self) -> None:
        '''
        Sometimes when testing, one needs to "click away" from, say, an input field to return to a neutral application state.
        For example, when typing into an input field, a pop-up may appear (for example when using the mask editor).
        You can use this method to implement a click away behaviour for your page object.
        '''
        raise NotImplementedError