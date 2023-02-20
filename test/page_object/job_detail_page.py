"""Page object representing details page of a job.
Exports single class--the aforementioned page object.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, List

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.relative_locator import locate_with

from page_object.common.page_object import PageObject

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
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'table').below({By.XPATH:'//span[text()="Hashes"]'})   # type: ignore
        )

    @property
    def __job_state_text(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR,'.status')

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
