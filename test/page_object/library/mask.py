from __future__ import annotations
from typing import TYPE_CHECKING, List, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.relative_locator import locate_with
from selenium.common.exceptions import NoSuchElementException

from page_object.common.page_object import PageObject
from page_object.common.exception import InvalidStateError
from page_object.table.mask_management_row import MaskManagementRow
from page_object.table.table_manipulation import load_table_elements

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement
    from pathlib import Path


class MaskManagement(PageObject):
    def ensure_loaded(self):
        WebDriverWait(self.driver,30,ignored_exceptions={InvalidStateError,NoSuchElementException}).until(
            lambda driver:
                driver.find_element(By.XPATH,'//*[contains(@class, "v-card__title") and text()[contains(.,"Mask sets")]]')
                and len(self.get_available_mask_files()) != 0
        )

    @property
    def __mask_file_table(self) -> WebElement:
        return self.driver.find_element(By.TAG_NAME,'table')

    @property
    def __upload_form(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'form').below(self.__mask_file_table) #type: ignore
        )

    @property
    def __upload_button(self) -> WebElement:
        return self.__upload_form.find_element(By.CSS_SELECTOR,'button.primary--text')

    @property
    def __file_input(self) -> WebElement:
        return self.__upload_form.find_element(By.TAG_NAME,'input')

    def get_available_mask_files(self) -> List[MaskManagementRow]:
        return load_table_elements(self.driver,self.__mask_file_table,MaskManagementRow)

    def upload_mask_file(self,filename:Union[str,Path]) -> None:
        self.__file_input.send_keys(str(filename))
        self.__upload_button.click()
        self.get_snackbar_notification(raise_exception_on_error=True)
        self._wait_until_snackbar_notification_disappears()
