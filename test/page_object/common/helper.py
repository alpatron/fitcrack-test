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
from typing import TYPE_CHECKING, Union, overload, Callable, TypeVar, List

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests

from page_object.common.exception import InvalidStateError

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement
    from selenium.webdriver.support.relative_locator import RelativeBy
    X = TypeVar('X')


def click_away(driver:WebDriver) -> None:
    """Sometimes when testing, one needs to "click away" from, say, an input field to return
    to a neutral application state. For example, when typing into an input field, a pop-up
    may appear (for example when using the mask editor). You can use this method to
    implement a click away in such cases.

    This method should work in almost all cases. One exception is dialogs--
    in dialogs, this function closes the dialog (it clicks away from the dialog).
    The other exception is the login page, where the element this method relies on does not exist.
    But there is no need to use that function there.
    """
    ActionChains(driver).click(driver.find_element(By.CSS_SELECTOR,'header .v-toolbar__title')).perform() # ActionsChains is used to disregard the additional checks the standard element.click() performs.

def click_away_dialog(driver:WebDriver) -> None:
    """Same as `click_away` but for use when in dialog windows.
    (The normal click_away would close the dialog).
    """
    ActionChains(driver).click(driver.find_element(By.CSS_SELECTOR,'.v-dialog--active .v-card__title')).perform() # ActionsChains is used to disregard the additional checks the standard element.click() performs.

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
    scroll_into_view_workaround(element)
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


def scroll_into_view_workaround(element:WebElement) -> None:
    """Scrolls an element into view and actually works.
    This workaround is neccessary because the current version of Selenium has broken scroll
    support in the Actions API in Firefox; the screenshot_as_base64 call forces a scroll using
    some old and reliable way.
    """
    _ = element.screenshot_as_base64
    

@overload
def download_file_webadmin(driver:WebDriver, link:str, as_binary:bool=False) -> str: ...
@overload
def download_file_webadmin(driver:WebDriver, link:str, as_binary:bool=True) -> bytes: ...
def download_file_webadmin(driver:WebDriver, link:str, as_binary:bool=False) -> Union[bytes,str]:
    """Downloads a file given a link to it. Handles Webadmin authentication.
    Returns a `str` object of the file by default.
    The string decoding is left to the `requests` library.
    Line endings are then (after the string decoding) normalised to `\n`.

    Set parameter `as_binary=True` to get a `bytes` object.
    
    Selenium does not support file downloads, so we need to do downloads ourselves.
    """
    jwt = driver.execute_script('return localStorage.getItem("jwt");')
    cookies = {x['name']:x['value'] for x in driver.get_cookies()}
    response = requests.get(link,cookies=cookies,headers={'Authorization': f'Bearer {jwt}'})
    if as_binary:
        return response.content
    else:
        return response.text.replace('\r\n', '\n').replace('\r', '\n')


def predicate_in_list(predicate:Callable[[X],bool],list:List[X]) -> X:
    """Returns the first instance in an iterable that satisfies the predicate.
    ValueError is raised if no element is found.
    """
    try:
        return next((x for x in list if predicate(x)))
    except StopIteration:
        raise ValueError('No element that matches predicate found.')
    

def near_locator_distance_workaround(relative_locator:RelativeBy,element:WebElement,distance:int=100000) -> None:
    """`locate_with(locator).near(...)` should support specifying the search distance
    but (as of Selenium 4.8.0) seems that it doesn't.
    
    This function acts like `.near` but adds the option of specifying the search distance.
    `relative_locator` is the output of `locate_with`, `element` is the element near which to
    locate, and `distance` is the search distance.

    Default distance is set 100 000 px, to make the locator behave as if if there were no
    search limit (unless you have a very very large screen).
    """
    relative_locator.filters.append({"kind": "near", "args": [element,distance]})