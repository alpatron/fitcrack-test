"""Page object representing a row in a host-selection table.
Exports single class--the aforementioned page object.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from page_object.table.generic_enableable_table_row import GenericEnableableTableRow

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class HostSelection(GenericEnableableTableRow):
    """This class represents a row from a host-selection table,
    like the one on the Add Job page or the Job Detail page.
    """
    @property
    def __name_field(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(2) a')

    @property
    def __ip_address_field(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(3)')

    @property
    def __os_field(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(4)')

    @property
    def __processor_field(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(5)')
    
    @property
    def __active_jobs_field(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(6)')
    
    @property
    def __online_field(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(7)')

    @property
    def name(self) -> str:
        """The file name of the host."""
        return self.__name_field.text

    @property
    def ip_address(self) -> str:
        """The IP address of the host."""
        return self.__ip_address_field.text
    
    @property
    def operating_system(self) -> str:
        """The operating system of the host."""
        return self.__os_field.text
    
    @property
    def processor(self) -> str:
        """The processor of the host."""
        return self.__processor_field.text
    
    @property
    def active_jobs(self) -> int:
        """The number of active jobs asigned to the host."""
        return int(self.__active_jobs_field.text)
    
    @property
    def online_status(self) -> str:
        """The online-status of the host. Is "online" if the host is online;
        otherwise it should contain "N days ago" or some such, as shown in Webadmin.
        """
        try:
            self.__online_field.find_element(By.CLASS_NAME,'mdi-power')
            return 'online'
        except NoSuchElementException:
            return self.__online_field.text
