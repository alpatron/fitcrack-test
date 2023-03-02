"""Module containing the base GenericEnableableTableRow class for dealing with Webadmin tables."""

from __future__ import annotations
from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By

from page_object.common.page_object import PageComponentObject
from page_object.common.helper import download_file_webadmin

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class GenericLibraryTableRow(PageComponentObject):
    @property
    def __download_button(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:last-child a')
    
    @property
    def __delete_button(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:last-child input')
    
    @property
    def _name_link(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:first-child a')

    @property
    def name(self) -> str:
        return self._name_link.text

    def delete(self) -> None:
        self.__delete_button.click()

    def download(self) -> bytes:
        return download_file_webadmin(self.driver,self.__download_button.get_attribute('href'))
