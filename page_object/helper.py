from __future__ import annotations

from selenium.webdriver import ActionChains

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement

def obstructedClickWorkaround(driver:WebDriver, element:WebElement):
    '''
    Sometimes in Fitcrack Webadmin, some elements cannot be clicked using the default element.click() method in Selenium.
    This happens when dealing with checkboxes and radio buttons: a "fancy" ripple effect "obstructs" the actual checkbox/radio button,
    causing Selenium to think that the element would not actually get clicked, throwing an exception.

    This is a workaround for this problem. This function performs a click on an element using the low-level Actions API,
    bypassing the checks of the regular element.click() method.

    This function tries to scroll to the element and then clicks on the location of that element, performing no interactability checks.
    Do note this means really no interactability checks, not just the obstruction; i.e. including the things like visibility
    and whether an input element is enabled.
    '''

    _ = element.screenshot_as_base64 #Workaround because the current version of Selenium has broken scroll support in the Actions API in Firefox; the screenshot_as_base64 call forces a scroll using some old and reliable way.
    ActionChains(driver).click(element).perform() 