"""This module provides useful functions for handling tables in Webadmin.

build_table_selection_objects_from_table --
constructing page objects representing rows from a table

activate_elements_from_table_by_list_lookup --
activating specific table rows
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Callable, List, TypeVar, Type

from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException

from page_object.common.helper import click_away
from page_object.common.exception import InvalidStateError

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement
    from page_object.table.generic_enableable_table_row import GenericEnableableTableRow
    from page_object.common.page_object import T_PageComponentObject
    X = TypeVar('X')
    T_GenericTableSelection = TypeVar('T_GenericTableSelection',bound=GenericEnableableTableRow)


def build_table_row_objects_from_table(driver:WebDriver, table:WebElement,constructor:Type[T_PageComponentObject]) -> List[T_PageComponentObject]:
    """Given a table in Webadmin, constructs PageComponentObject for each row (each <tr> element)
    using the supplied constructor and returns a list of these objects.

    Essentially, if I have a table in WebAdmin, like the table of dictionaries in dictionary-attack
    settings, whose rows are represented by the DictionarySelection class, this function can parse
    the table and return a list of page objects of all the rows.

    The usage example for that is:
    `build_table_selection_objects_from_table(driver,table_element,DictionarySelection)`.

    You might also want to take a look at `load_table_elements`, which provides
    additional robustness checks.
    """
    return [constructor(driver,tableRow) for tableRow in table.find_elements(By.CSS_SELECTOR,'tbody tr')]


def activate_elements_from_table_by_list_lookup(table_rows:List[T_GenericTableSelection],lookup_value_getter:Callable[[T_GenericTableSelection],X],lookup_values:List[X]):
    """Given a list of table-row objects, selects a subset of those to be active.
    Which rows are activated depends on `lookup_values` and `lookup_value_getter`.
    `lookup_value_getter` is a function that takes a row and produces some value (usually a string).
    `lookup_values` is a list (or other iterable) of values that can be produced by the getter.
    Only rows that produce a values using the getter that is contained in
    `lookup_values` are activated.

    Sounds complicated because this is a generic function, but isn't really. Here's an example:

    I have the a dictionary table and I want the rows with the dictionaries named "foo" and "bar".
    The objects that represent the rows are in a list called `row_objects`.
    In that case, `lookup_value_getter` is a function that returns the name of dictionary.
    And `lookup_values` is a list of the names I want. So the call is:
    `activate_elements_from_table_by_list_lookup(row_objects,lambda x:x.name,['foo','bar'])`

    Raises InvalidStateError if not all requested table rows could be activated.
    """
    found_wanted_rows = list(filter(lambda x: lookup_value_getter(x) in lookup_values, table_rows))
    if len(found_wanted_rows) != len(lookup_values): #TODO: Possibly there could be also duplicate names; do we want to check for those?
        raise InvalidStateError('Some requested rows do not exist in the table.\n')
    for row in found_wanted_rows:
        row.enabled = True


def show_as_many_rows_per_table_page_as_possible(driver:WebDriver,table:WebElement) -> None:
    rows_per_page_dropdown_button = driver.find_element(
        locate_with(By.CLASS_NAME,'v-select__slot').below(table) #type: ignore
    )
    
    rows_per_page_dropdown_button.click()

    rows_per_page_dropdown_largest_choice = driver.find_element(
        locate_with(By.CSS_SELECTOR,'.v-list>div:last-child').near(rows_per_page_dropdown_button) #type: ignore
    )

    rows_per_page_dropdown_largest_choice.click()


def load_table_elements(driver:WebDriver,table:WebElement,constructor:Type[T_PageComponentObject]) -> List[T_PageComponentObject]:
    """Works like `build_table_row_objects_from_table`, but provides more checks:
    
    Ensures that the table shows as many rows as possible by using the "rows per page" selection.
    This means the table could show all elements (e.g. the dictionary table in the Add Job page),
    or it could mean the table could show a big but limited number
    (e.g. the dictionary table in the Library->Dictionary page can show at most 50 rows).
    For testing, this should not be an issue since no test expects such a large number of rows
    to be present, and implementing support for interacting with pagination would add needless
    complexity.

    Correctly handles the case that no rows are present and returns an empty list then.

    Raises an InvalidStateError if the table is in the middle of the initial load.

    Retries up to ten times to load the table elements (if a row is loaded in or removed as the
    function is running, WebDriver emits a StaleElementException as the
    previously existing <tr> elements cease to exist). If it fails even after ten tries,
    raises an InvalidStateError.
    """
    click_away(driver) #Any previous call to show_as_many_rows_per_table_page_as_possible may have left an open selection box; we need to close it.
    show_as_many_rows_per_table_page_as_possible(driver,table)
    for _ in range(10):
        try:
            td_elements_in_table = table.find_elements(By.TAG_NAME,'td')
            if len(td_elements_in_table) == 1:
                if td_elements_in_table[0].text == 'No data available':
                    return []
                if td_elements_in_table[0].text == 'Loading items...':
                    raise InvalidStateError('Table elements have not loaded yet.')
            return build_table_row_objects_from_table(driver,table,constructor)
        except StaleElementReferenceException:
            ActionChains(driver).pause(2).perform()
    raise InvalidStateError(
        'Failed to load table elements. '
        'Retried ten times but keep getting StaleElementReferenceExceptions. '
        'Page objects or Webadmin may be broken.'
    )