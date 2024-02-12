"""Module containing the base GenericEnableableTableRow class for dealing with Webadmin tables."""

from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from selenium.webdriver.common.by import By

from page_object.common.page_object import PageComponentObject

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class CrackedHashTableRow(PageComponentObject):
    @property
    def __hash(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(1)')

    @property
    def __password(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(2) span')

    @property
    def __cracked_time(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(3)')

    @property
    def password_hash(self) -> str:
        return self.__hash.text

    @property
    def password(self) -> Optional[str]:
        if 'red--text' in self.__password.get_attribute('class'): # type: ignore
            return None
        return self.__password.text

    @property
    def cracked_time(self) -> str:
        return self.__cracked_time.text
