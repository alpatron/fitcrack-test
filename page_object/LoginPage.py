from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import JavascriptException, NoSuchElementException
from selenium.webdriver.support.relative_locator import locate_with
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement

from page_object.PageObject import PageObject
from page_object.Dashboard import Dashboard
from page_object.Sidebar import SideBar
from page_object.helper import clearWorkaround

class LoginPage(PageObject):
    URL_PATH = '/login'
    
    def ensure_loaded(self):
        WebDriverWait(self.driver,30,ignored_exceptions={JavascriptException, NoSuchElementException}).until(lambda _:self.username_field)

    @property
    def username_field(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'input').near({By.XPATH:'//label[text()="Username"]'})  # type: ignore
        )

    @property
    def password_field(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'input').near({By.XPATH:'//label[text()="Password"]'})  # type: ignore
        )

    @property
    def submit_button(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR,'button[type="submit"]')

    def navigate(self,prefix:str) -> None:
        self.driver.get(prefix+self.URL_PATH)

    def login(self,username:str,password:str) -> tuple[SideBar,Dashboard]:
        clearWorkaround(self.username_field)    #The order of clearing and typing is important here.
        clearWorkaround(self.password_field)    #The clear workaround does not (and cannot easily) perform an unfocusing operation at the end of the clearing action.
        self.username_field.send_keys(username) #This means that after clearing a field, the label inside the input disappears... wait... this whole isn't robust and this is just
        self.password_field.send_keys(password) #the symptom, not the cause. What is needed is more robust locators here in general. *sigh* This is a todo.
        self.submit_button.click()
        return SideBar(self.driver), Dashboard(self.driver)
