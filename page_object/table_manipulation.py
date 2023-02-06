from __future__ import annotations

from selenium.webdriver.common.by import By

from typing import TYPE_CHECKING, Callable, List, TypeVar, Type
if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement
    from page_object.GenericTableSelection import GenericTableSelection
    X = TypeVar('X')
    T_GenericTableSelection = TypeVar('T_GenericTableSelection',bound=GenericTableSelection)


def buildTableSelectionObjectsFromTable(driver:WebDriver, table:WebElement,constructor:Type[T_GenericTableSelection]) -> List[T_GenericTableSelection]:
    return [constructor(driver,tableRow) for tableRow in table.find_elements(By.CSS_SELECTOR,'tbody tr')]

def activateElementsFromTableByListLookup(tableRows:List[T_GenericTableSelection],lookup_value_getter:Callable[[T_GenericTableSelection],X],lookup_values:List[X]):
    found_wanted_rows = list(filter(lambda x: lookup_value_getter(x) in lookup_values, tableRows))
    if len(found_wanted_rows) != len(lookup_values): #TODO: Possibly there could be also duplicate names; do we want to check for those?
        raise Exception('Some requested dictionaries do not exist in the table.\n')
    for row in found_wanted_rows:
        row.selected = True