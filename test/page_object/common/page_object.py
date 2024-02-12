"""Module containing the base page-object class."""

from __future__ import annotations
from typing import TYPE_CHECKING, TypeVar

from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.expected_conditions import invisibility_of_element, visibility_of
from selenium.webdriver.common.by import By

from page_object.common.webadmin_snackbar_notifcation import WebadminSnackbarNotification, WebadminSnackbarNotificationType
from page_object.common.exception import InvalidStateError, WebadminError

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement
    T_PageComponentObject = TypeVar('T_PageComponentObject',bound=PageComponentObject) #type: ignore

class PageObject:
    """This is the base class of all page objects.
    Page objects represent individual pieces of the UI and expose methods that model user
    interactions, like "login", "set job name", "create job" etc.

    This class provides some abstract methods and changes the behaviour of the __init__ method
    for use in page objects.

    To create a page object, one needs to pass a Selenium WebDriver instance.
    When creating a page object, the `ensure_loaded` method is automatically run to wait until
    the UI is loaded (this method needs to be implemented for each page object;
    see the `ensure_loaded` doc string). You can suppress the running of `ensure_loaded` by
    specifying using the parameter `no_ensure_loaded=True` when creating a page object.
    This is necessary when creating the first object in a script, as the web browser starts on
    blank page.
    """

    def __init__(self,driver:WebDriver,no_ensure_loaded=False):
        self.driver = driver
        if not no_ensure_loaded:
            self.ensure_loaded()

    def ensure_loaded(self) -> None:
        """Waits until the UI the page object models is loaded and it is safe to use the
        page object. This is an abstract method that can but need not be implemented.
        The default, non-overridden method performs no checks and returns immediately.
        
        This methods should return if and only if the state of the web app is ready,
        and it should raise an exception if the UI isn't ready within a time limit.
        """

    @property
    def _snackbar_notification_text(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR,'.errorSnackbar .v-alert__content')
    
    @property
    def _dialog_window(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR,'.v-dialog--active')

    def _wait_until_snackbar_notification_disappears(self) -> None:
        try:
            WebDriverWait(self.driver,10).until(invisibility_of_element(self._snackbar_notification_text))
        except NoSuchElementException:
            pass

    def _wait_until_dialog_closes(self,timeout:float=10) -> None:
        try:
            WebDriverWait(self.driver,timeout).until(invisibility_of_element(self._dialog_window))
        except NoSuchElementException:
            pass

    def get_snackbar_notification(self,raise_exception_on_error:bool=False) -> WebadminSnackbarNotification:
        WebDriverWait(self.driver,10).until(visibility_of(self._snackbar_notification_text))
        helper_element = self.driver.find_element(By.CSS_SELECTOR, '.errorSnackbar .v-alert')
        element_classes = helper_element.get_attribute('class')
        error = 'error' in element_classes # type: ignore
        success = 'success' in element_classes # type: ignore
        match (success, error):
            case (True, False):
                snackbar_notification_type = WebadminSnackbarNotificationType.SUCCESS
            case (False, True):
                snackbar_notification_type = WebadminSnackbarNotificationType.ERROR
            case _:
                raise InvalidStateError('Could not determine the type of snackbar notification.')
        notification_text = self._snackbar_notification_text.text
        if raise_exception_on_error and snackbar_notification_type == WebadminSnackbarNotificationType.ERROR:
            raise WebadminError(notification_text)
        return WebadminSnackbarNotification(snackbar_notification_type,notification_text)


class PageComponentObject(PageObject):
    """Specialised page-object class for page-component objects.
    These objects also hold an `_element` property containing a WebElement of the component
    that is being modelled alongside the `_driver` property of the standard PageObject class.
    
    This is useful when there are many similar components on a page an we want to
    locate sub-elements within them.
    
    For example, there are many table rows in a table, we can have a PageComponentObject
    for every row, setting the _element property to the <tr> element. We can then have
    locators for each column in the form of
    `self._element.find_element(By.CSS_SELECTOR,'td:nth-child(1)')`
    for the first column (first <td>) element. This allows us to not use clunky
    global locators that search through the entire document's DOM tree.
    """
    def __init__(self,driver:WebDriver,element:WebElement):
        super().__init__(driver)
        self._element = element