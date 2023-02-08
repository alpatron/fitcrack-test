from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from typing import TYPE_CHECKING, List
from selenium.webdriver.support.relative_locator import locate_with
if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement

from page_object.PageObject import PageObject

class JobDetailPage(PageObject):

    def ensure_loaded(self):
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

    def getHashes(self) -> List[tuple[str,str]]:
        return [
            (
                tableRow.find_element(By.CSS_SELECTOR,'td:nth-child(1)').text,
                tableRow.find_element(By.CSS_SELECTOR,'td:nth-child(2)').text
            ) for tableRow in self.__hash_table.find_elements(By.CSS_SELECTOR,'tbody tr')
        ]
    
    def start_job(self) -> None:
        self.__start_button.click()

    def stop_job(self) -> None:
        self.__stop_button.click()

    def get_job_state(self) -> str:
        return self.__job_state_text.text
    