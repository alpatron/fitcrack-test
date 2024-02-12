"""Page object representing brute-force-attack settings in the Add Job page.
Exports two classes:
BruteForceAttackSettings -- the aforementioned page object
MarkovMode --
enum of all the possible values that the Markov mode can be set to in this attack mode
"""

from __future__ import annotations
from typing import TYPE_CHECKING, List
from enum import Enum
import itertools

from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from page_object.common.page_object import PageObject
from page_object.table.charset_selection import CharsetSelection
from page_object.table.markov_file_selection import MarkovFileSelection
from page_object.table.mask_file_selection_row import MaskFileSelection
from page_object.table.table_manipulation import build_table_row_objects_from_table, activate_elements_from_table_by_list_lookup, show_as_many_rows_per_table_page_as_possible
from page_object.common.helper import obstructed_click_workaround, clear_workaround, click_away
from page_object.common.exception import InvalidStateError

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class MarkovMode(Enum):
    """Enum describing the state of the Markov-mode selection
    in the brute-force-attack settings panel in the Add Job page.
    
    The enum values (e.g. the lowercase 'markov-disabled') are set to the strings
    that should be used in the test configuration files.
    """
    MARKOV_DISABLED = 'markov-disabled'
    MARKOV_2D = 'markov-2d'
    MARKOV_3D = 'markov-3d'


class BruteForceAttackSettings(PageObject):
    """This class represents the brute-force-attack settings in the Create Job page."""

    def ensure_loaded(self):
        """Waits until charsets and markov files are loaded, then waits for five more seconds
        for vuejs to settle and finish all animations and DOM manipulation.
        """
        try:
            WebDriverWait(self.driver,30).until(lambda _: len(self.get_available_charsets()) != 0 and len(self.get_available_markov_files()) != 0)
            ActionChains(self.driver).pause(5).perform()
        except TimeoutException:
            pass

    def __get_mask_input_field(self,index:int) -> WebElement:
        return self.driver.find_element(By.ID,f'mask-{index}-mask-input')

    def __get_mask_remove_button(self,index:int) -> WebElement:
        return self.driver.find_element(By.ID,f'mask-{index}-mask-remove')

    @property
    def __add_mask_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'add-mask-button')

    @property
    def __charset_selection_table(self) -> WebElement:
        return self.driver.find_element(By.XPATH,'//span[text()[contains(.,"Select charsets (max. 4)")]]/ancestor::div[contains(@class, "col")][1]//table')

    @property
    def __markov_selection_table(self) -> WebElement:
        return self.driver.find_element(By.XPATH,'//span[text()[contains(.,"Markov file")]]/ancestor::div[contains(@class, "col")][1]//table')

    @property
    def __markov_threshold_input(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'input').near({By.XPATH:'//label[text()="Markov threshold"]'})  # type: ignore
        )

    @property
    def __markov_disabled_radio_button(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'input').to_left_of({By.XPATH:'//label[text()="Markov disabled"]'})  # type: ignore
        )

    @property
    def __2D_markov_radio_button(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'input').to_left_of({By.XPATH:'//label[text()="2D Markov"]'})  # type: ignore
        )

    @property
    def __3D_markov_radio_button(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'input').to_left_of({By.XPATH:'//label[text()="3D Markov"]'})  # type: ignore
        )

    @property
    def __load_mask_button(self) -> WebElement:
        return self.driver.find_element(By.XPATH,'//span[text()[contains(.,"Load masks")]]')

    @property
    def __mask_dialog_table(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR,'.v-dialog--active table')

    @property
    def __mask_dialog_load_button(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR,'.v-dialog--active button.primary')

    def get_available_charsets(self) -> List[CharsetSelection]:
        """Returns a list of CharsetSelection page objects representing the custom charsets
        that can be chosen.
        """
        click_away(self.driver)
        show_as_many_rows_per_table_page_as_possible(self.driver,self.__charset_selection_table)
        return build_table_row_objects_from_table(self.driver,self.__charset_selection_table,CharsetSelection)

    def get_available_markov_files(self) -> List[MarkovFileSelection]:
        """Returns a list of MarkovFileSelection page objects representing the markov-statistics
        files that can be used for Markov ordering.
        """
        click_away(self.driver)
        show_as_many_rows_per_table_page_as_possible(self.driver,self.__markov_selection_table)
        return build_table_row_objects_from_table(self.driver,self.__markov_selection_table,MarkovFileSelection)

    def get_available_mask_files(self) -> List[str]:
        """Returns the names (strings) of all mask files that can be loaded."""
        self.__load_mask_button.click()
        ActionChains(self.driver).pause(4).perform() # Wait for animation to finish
        show_as_many_rows_per_table_page_as_possible(self.driver,self.__mask_dialog_table)
        mask_files = build_table_row_objects_from_table(self.driver,self.__mask_dialog_table,MaskFileSelection)
        mask_names = [mask_file.name for mask_file in mask_files]
        click_away(self.driver)
        return mask_names

    def load_mask_file(self,mask_file_name:str) -> None:
        """Loads the mask file with the given name."""
        self.__load_mask_button.click()
        ActionChains(self.driver).pause(4).perform() # Wait for animation to finish
        show_as_many_rows_per_table_page_as_possible(self.driver,self.__mask_dialog_table)
        mask_files = build_table_row_objects_from_table(self.driver,self.__mask_dialog_table,MaskFileSelection)
        activate_elements_from_table_by_list_lookup(mask_files,lambda x: x.name,[mask_file_name])
        self.__mask_dialog_load_button.click()

    def select_charsets(self,wanted_charsets:List[str]) -> None:
        """Given a list of charset names (as they appear in the name column), selects the charsets
        with those names to be used. Raises exception on failure.
        """
        activate_elements_from_table_by_list_lookup(self.get_available_charsets(),lambda x:x.name,wanted_charsets)

    def select_markov_file(self,markov_file:str) -> None:
        """Given the name of a Markov statistics file, selects this file to be used.
        Raises exception on failure.
        """
        activate_elements_from_table_by_list_lookup(self.get_available_markov_files(),lambda x:x.name,[markov_file])

    def get_selected_markov_mode(self) -> MarkovMode:
        """Returns which Markov mode is selected (which radio button is pressed).
        Raises InvalidStateError if the state could need be determined.
        """
        markov_disabled_checked = self.__markov_disabled_radio_button.get_attribute('aria-checked')
        markov_2d_checked = self.__2D_markov_radio_button.get_attribute('aria-checked')
        markov_3d_checked = self.__3D_markov_radio_button.get_attribute('aria-checked')

        match (markov_disabled_checked,markov_2d_checked,markov_3d_checked):
            case ('true', 'false', 'false'):
                return MarkovMode.MARKOV_DISABLED
            case ('false', 'true', 'false'):
                return MarkovMode.MARKOV_2D
            case ('false', 'false', 'true'):
                return MarkovMode.MARKOV_3D
            case _:
                raise InvalidStateError(
                    'Invalid state of Markov-mode radio button '
                    '(either no mode is selected or more than one mode is selected at once).'
                )

    def select_markov_mode(self, markov_mode:MarkovMode) -> None:
        """Selects a Markov mode to be used. Takes as input a MarkovMode enum object."""
        match markov_mode:
            case MarkovMode.MARKOV_DISABLED:
                obstructed_click_workaround(self.driver,self.__markov_disabled_radio_button)
            case MarkovMode.MARKOV_2D:
                obstructed_click_workaround(self.driver,self.__2D_markov_radio_button)
            case MarkovMode.MARKOV_3D:
                obstructed_click_workaround(self.driver,self.__3D_markov_radio_button)

    def set_markov_threshold_value(self,threshold:int) -> None:
        """Sets the markov threshold value. Method takes an int."""
        clear_workaround(self.__markov_threshold_input)
        self.__markov_threshold_input.send_keys(str(threshold))

    def set_mask_value(self,mask_value:str,index:int) -> None:
        """Sets the value of the mask with given index. Masks are indexed from the bottom of the UI
        and start at 0 (i.e. 0 is the bottom-most mask). Raises InvalidStateError if the mask input
        doesn't exist/couldn't be found.
        """
        try:
            clear_workaround(self.__get_mask_input_field(index))
            self.__get_mask_input_field(index).send_keys(mask_value)
        except NoSuchElementException as exc:
            raise InvalidStateError(
                f'There is no mask with index {index}. This may simply mean that the `add_mask` '
                 'method was not called and so there is only one mask input in the UI. It could '
                 'also mean a broken page object/broken Webadmin.'
            ) from exc

    def add_mask_input(self) -> None:
        """Adds a mask input; i.e. presses the add mask button."""
        self.__add_mask_button.click()

    def remove_mask(self,index:int) -> None:
        """Removes a mask at the given index. Masks are indexed from the bottom of the UI
        and start at 0 (i.e. 0 is the bottom-most mask).
        
        Do note that removing a mask retroactively changes the mask order:
        if there are three masks with indexes 0, 1, 2, then removing mask with index 1
        causes mask with index 2 to become mask with index 1 (so the behaviour is the same
        as removing elements from an array.).
        """
        try:
            self.__get_mask_remove_button(index).click()
        except NoSuchElementException as exc:
            raise InvalidStateError(
                'Could not remove mask because its remove button could not be found. '
                'This can happen if there is only one mask; in those cases, the remove button '
                'is not shown and thus the mask cannot be removed. If this is not the case, '
                'this may indicate a broken page object/broken Webadmin.'
            ) from exc

    def get_all_input_masks(self) -> List[str]:
        """Returns a list of strings of all the masks that are input in the UI.
        First in the list is the mask at the bottom in the UI.
        """
        input_masks = list()
        for i in itertools.count():
            try:
                input_masks.append(self.__get_mask_input_field(i).get_attribute('value'))
            except NoSuchElementException:
                break
        return input_masks

    def set_masks_from_list(self,masks:List[str]) -> None:
        """Given a list of strings representing masks, sets those as input for the attack.
        Removes all potentially pre-existing masks.
        """
        number_of_already_input_masks = len(self.get_all_input_masks())
        for i in range(number_of_already_input_masks-1,0,-1): #Removes masks in reverser order; from top to bottom in the UI.
            self.remove_mask(i)
        for i, mask in zip(itertools.count(), masks):
            if i > 0:
                self.add_mask_input()
            self.set_mask_value(mask,i)
            click_away(self.driver)
