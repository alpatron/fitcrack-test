"""This module provides useful functions for handling tables in Webadmin.

build_table_selection_objects_from_table --
constructing page objects representing rows from a table

activate_elements_from_table_by_list_lookup --
activating specific table rows
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Callable, List, TypeVar, Type

from selenium.webdriver.common.by import By

from page_object.common.exception import InvalidStateError

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement
    from page_object.table.generic_table_selection import GenericTableSelection
    X = TypeVar('X')
    T_GenericTableSelection = TypeVar('T_GenericTableSelection',bound=GenericTableSelection)


def build_table_selection_objects_from_table(driver:WebDriver, table:WebElement,constructor:Type[T_GenericTableSelection]) -> List[T_GenericTableSelection]:
    """Given a table in Webadmin whose rows can be modelled by GenericTableSelection
    (or subclass thereof) objects, and the specific class that is to be used for modelling the
    rows of that table, returns a list of page objects representing these rows.

    Essentially, if I have a table in WebAdmin, like the table of dictionaries in dictionary-attack
    settings, whose rows are represented by the DictionarySelection class, this function can parse
    the table and return a list of page objects of all the rows.

    The usage example for that is:
    `build_table_selection_objects_from_table(driver,table_element,DictionarySelection)`.
    """
    return [constructor(driver,tableRow) for tableRow in table.find_elements(By.CSS_SELECTOR,'tbody tr')]


def activate_elements_from_table_by_list_lookup(table_rows:List[T_GenericTableSelection],lookup_value_getter:Callable[[T_GenericTableSelection],X],lookup_values:List[X]):
    """Given a list of table-row objects, selects a subset of those to be active.
    Which rows are activated depends on `lookup_values` and `lookup_value_getter`.
    `lookup_value_getter` is a function that takes a row and produces some value (usually a string).
    `lookup_values` is a list (or other iterable) of values that can be produced by the getter.
    Only rows that produce a values using the getter that is contained in
    `lookup_values` are activated.

    Sounds complicated because this isa generic function, but isn't really. Here's an example:

    I have the a dictionary table and I want the rows with the dictionaries named "foo" and "bar".
    The objects that represent the rows are in a list called `row_objects`.
    In that case, `lookup_value_getter` is a function that returns the name of dictionary.
    And `lookup_values` is a list of the names I want. So the call is:
    `activate_elements_from_table_by_list_lookup(row_objects,lambda x:x.name,['foo','bar'])`

    Raises InvalidStateError if not all requested table rows could be activated.
    """
    found_wanted_rows = list(filter(lambda x: lookup_value_getter(x) in lookup_values, table_rows))
    if len(found_wanted_rows) != len(lookup_values): #TODO: Possibly there could be also duplicate names; do we want to check for those?
        raise InvalidStateError('Some requested dictionaries do not exist in the table.\n')
    for row in found_wanted_rows:
        row.selected = True
