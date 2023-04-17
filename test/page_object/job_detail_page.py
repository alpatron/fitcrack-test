"""Page object representing details page of a job.
Exports single class--the aforementioned page object.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, List

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver import ActionChains

from page_object.common.page_object import PageObject, PageComponentObject
from page_object.common.helper import click_away
from page_object.table.host_selection import HostSelection
from page_object.table.table_manipulation import build_table_row_objects_from_table, activate_elements_from_table_by_list_lookup, load_table_elements

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class JobDetailPage(PageObject):
    """Represents the page showing the details of specific job."""

    def ensure_loaded(self):
        """Waits until the state of the job appears on the page."""
        WebDriverWait(self.driver,30).until(lambda _: self.get_job_state() != '')

    @property
    def __start_button(self) -> WebElement:
        return self.driver.find_element(By.XPATH,'//span[text()[contains(.,"start")]]')

    @property
    def __stop_button(self) -> WebElement:
        return self.driver.find_element(By.XPATH,'//span[text()[contains(.,"stop")]]')

    @property
    def __hash_table(self) -> WebElement:
        return self.driver.find_element(By.XPATH,'//span[text()[contains(.,"Hashes")]]/ancestor::div[contains(@class, "col")][1]//table')   

    @property
    def __job_state_text(self) -> WebElement:
        return self.driver.find_element(By.CLASS_NAME,'status')

    @property
    def __assign_hosts_button(self) -> WebElement:
        return self.driver.find_element(By.XPATH,'//span[text()[contains(.,"Assign Hosts")]]')

    @property
    def __assign_hosts_table(self) -> WebElement:
        return self._dialog_window.find_element(By.TAG_NAME,'table')

    @property
    def __assign_hosts_confirm_button(self) -> WebElement:
        return self._dialog_window.find_element(By.ID,'host-mapper-assign')

    @property
    def __active_hosts_table(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'table').above(self.__assign_hosts_button) #type: ignore
        ) 

    def get_hashes(self) -> List[tuple[str,str]]:
        """Return a list of tuples, where the first element is an input hash of the cracking job
        and the second element is the recovered password. If the password is not cracked, then
        the second element is an empty string."""
        return [
            (
                tableRow.find_element(By.CSS_SELECTOR,'td:nth-child(1)').text,
                tableRow.find_element(By.CSS_SELECTOR,'td:nth-child(2)').text
            ) for tableRow in self.__hash_table.find_elements(By.CSS_SELECTOR,'tbody tr')
        ]

    def start_job(self) -> None:
        """Start the job if the job is stopped."""
        self.__start_button.click()

    def stop_job(self) -> None:
        """Stops the job if the job is running."""
        self.__stop_button.click()

    def get_job_state(self) -> str:
        """Returns the state of the job as it's shown."""
        return self.__job_state_text.text

    def get_available_hosts(self) -> List[str]:
        self.__assign_hosts_button.click()
        hosts = build_table_row_objects_from_table(self.driver,self.__assign_hosts_table,HostSelection)
        host_names = [host.name for host in hosts]
        click_away(self.driver)
        return host_names

    def select_hosts_for_job(self,desired_hosts:List[str]) -> None:
        self.__assign_hosts_button.click()
        ActionChains(self.driver).pause(4).perform() #Wait for animation to finish
        hosts = build_table_row_objects_from_table(self.driver,self.__assign_hosts_table,HostSelection)
        activate_elements_from_table_by_list_lookup(hosts,lambda x: x.name, desired_hosts)
        self.__assign_hosts_confirm_button.click()
        self._wait_until_dialog_closes()
        self.get_snackbar_notification(raise_exception_on_error=True)
        self._wait_until_snackbar_notification_disappears()

    def get_active_hosts(self) -> List[ActiveHostEntry]:
        return load_table_elements(self.driver,self.__active_hosts_table,ActiveHostEntry,no_element_text='None assigned',no_ensure_most=True)

    def check_if_job_finished(self) -> bool:
        return self.get_job_state() in ['Finished','Exhausted']
    
    def wait_until_job_finished(self,timeout:float) -> None:
        WebDriverWait(self.driver,timeout).until(lambda _: self.check_if_job_finished())


class ActiveHostEntry(PageComponentObject):
    @property
    def __name_field(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(1) a')

    @property
    def __ip_address_field(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(2)')

    @property
    def __online_field(self) -> WebElement:
        return self._element.find_element(By.CSS_SELECTOR,'td:nth-child(3)')
    
    @property
    def name(self) -> str:
        """The file name of the host."""
        return self.__name_field.text

    @property
    def ip_address(self) -> str:
        """The IP address of the host."""
        return self.__ip_address_field.text
    
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