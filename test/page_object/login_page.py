"""Page object representing the login page.
Exports single class--the aforementioned page object.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import JavascriptException, NoSuchElementException
from selenium.webdriver.support.relative_locator import locate_with

from page_object.page_object import PageObject
from page_object.dashboard import Dashboard
from page_object.side_bar import SideBar
from page_object.helper import clear_workaround

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class LoginPage(PageObject):
    """Class representing the login page of Webadmin."""

    URL_PATH = '/login'

    def ensure_loaded(self):
        """Waits until the username field appears."""
        WebDriverWait(self.driver,30,ignored_exceptions={JavascriptException, NoSuchElementException}).until(lambda _:self.__username_field)

    @property
    def __username_field(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'input').near({By.XPATH:'//label[text()="Username"]'})  # type: ignore
        )

    @property
    def __password_field(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'input').near({By.XPATH:'//label[text()="Password"]'})  # type: ignore
        )

    @property
    def __submit_button(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR,'button[type="submit"]')

    def navigate(self,prefix:str) -> None:
        """Navigates to the the login page. `prefix` is the base URL where Webadmin runs.
        So for example https://www.fitcrack.com (no forward slash).
        """
        self.driver.get(prefix+self.URL_PATH)

    def login(self,username:str,password:str) -> tuple[SideBar,Dashboard]:
        """Logs into Fitcrack Webadmin with the given username and password.
        Returns a SideBar object and a Dashboard object.
        The current LoginPage object ceases to be useable.
        """
        clear_workaround(self.__username_field)    #The order of clearing and typing is important here.
        clear_workaround(self.__password_field)    #The clear workaround does not (and cannot easily) perform an unfocusing operation at the end of the clearing action.
        self.__username_field.send_keys(username)  #This means that after clearing a field, the label inside the input disappears... wait... this whole isn't robust and this is just
        self.__password_field.send_keys(password)  #the symptom, not the cause. What is needed is more robust locators here in general. *sigh* This is a todo.
        self.__submit_button.click()
        return SideBar(self.driver), Dashboard(self.driver)
