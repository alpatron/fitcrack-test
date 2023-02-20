"""This module provides useful functions for using Selenium to test Webadmin.

obstructed_click_workaround --
for when the usual `element.click()` raises an exception and you want to ignore it and click anyway

get_checkbox_state --
querying checkedness state of Webadmin checkboxes since the usual way does not work

clear_workaround --
the usual `element.clear()` method does not work for Webadmin <input>s for some reason;
this should be used instead
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from page_object.common.exception import InvalidStateError

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement


def obstructed_click_workaround(driver:WebDriver, element:WebElement):
    """Sometimes in Fitcrack Webadmin, some elements cannot be clicked using the default
    element.click() method in Selenium. This happens when dealing with checkboxes and radio
    buttons: a "fancy" ripple effect "obstructs" the actual checkbox/radio button, causing
    Selenium to think that the element would not actually get clicked, throwing an exception.

    This is a workaround for this problem. This function performs a click on an element using
    the low-level Actions API, bypassing the checks of the regular element.click() method.

    This function tries to scroll to the element and then clicks on the location of that element,
    performing no interactability checks. Do note this means really no interactability checks, not
    just the obstruction; i.e. including the things like visibility and whether an input element
    is enabled.
    """
    _ = element.screenshot_as_base64
    #Workaround because the current version of Selenium has broken scroll support in the
    #Actions API in Firefox; the screenshot_as_base64 call forces a scroll using some old
    #and reliable way.
    ActionChains(driver).click(element).perform()


def get_checkbox_state(element:WebElement) -> bool:
    """Checkboxes in Webadmin do not have a simple "checked" property that can be used to garner
    the checkbox's state that when queried gives a simple bool. This function returns a bool giving
    the state of a Webadmin checkbox and raises an exception if the state cannot be determined.
    You need to supply the relevant <input> element of the checkbox you want to get its state of.
    """
    match element.get_attribute('aria-checked'):
        case 'true':
            return True
        case 'false':
            return False
        case _:
            raise InvalidStateError(
                'The selection state of a checkbox could not be determined.'
                'This may indicate a broken page object.'
            )


def clear_workaround(element:WebElement) -> None:
    """For some reason, the default `element.clear()` in Selenium does not work with inputs
    in Webadmin. This is a workaround function that works by sending CTRL+A followed by BACKSPACE,
    thus hopefully selecting everything and then deleting it.
    
    Do note that this thus does perform some of the checks and specialised behaviour of the regular
    clear method. So do check that you must use this workaround; if you do not, use the regular
    clear method."""
    element.send_keys(Keys.CONTROL+'A'+Keys.NULL)
    #Keys.NULL is necessary for performing chording; i.e. pressing multiple keys at once.
    #Selenium should offer a convenience method for chording, but the Python version does
    #not provide this. So we need to do this like so.
    element.send_keys(Keys.BACKSPACE)
