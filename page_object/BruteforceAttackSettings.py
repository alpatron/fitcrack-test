from __future__ import annotations

from enum import Enum
import itertools

from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement

from page_object.PageObject import PageObject
from page_object.CharsetSelection import CharsetSelection
from page_object.MarkovFileSelection import MarkovFileSelection
from page_object.table_manipulation import buildTableSelectionObjectsFromTable, activateElementsFromTableByListLookup
from page_object.helper import obstructedClickWorkaround

class MarkovMode(Enum):
    MARKOV_DISABLED = 'markov-disabled'
    MARKOV_2D = 'markov-2d'
    MARKOV_3D = 'markov-3d'

class BruteforceAttackSettings(PageObject):
    def ensure_loaded(self):
        try:
            WebDriverWait(self.driver,30).until(lambda _: len(self.getAvailableCharsets()) != 0 and len(self.getAvailableMarkovFiles()) != 0)
            ActionChains(self.driver).pause(5).perform()
        except TimeoutException:
            pass
    
    def _click_away(self) -> None:
        self.driver.find_element(By.XPATH,'//span[text()[contains(.,"Select charsets (max. 4)")]]').click()

    def __get_mask_input_field(self,index:int) -> WebElement:
        return self.driver.find_element(By.ID,f'mask-{index}-mask-input')

    def __get_mask_remove_button(self,index:int) -> WebElement:
        return self.driver.find_element(By.ID,f'mask-{index}-mask-remove')

    @property
    def __add_mask_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'add-mask-button')

    @property
    def __charset_selection_table(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'table').below({By.XPATH:'//span[text()[contains(.,"Select charsets (max. 4)")]]'})  # type: ignore
        )

    @property
    def __markov_selection_table(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'table').below({By.XPATH:'//span[text()[contains(.,"Markov file")]]'})  # type: ignore
        )

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

    def getAvailableCharsets(self) -> List[CharsetSelection]:
        return buildTableSelectionObjectsFromTable(self.driver,self.__charset_selection_table,CharsetSelection)

    def getAvailableMarkovFiles(self) -> List[MarkovFileSelection]:
        return buildTableSelectionObjectsFromTable(self.driver,self.__markov_selection_table,MarkovFileSelection)

    def selectCharsets(self,wanted_charsets:List[str]) -> None:
        activateElementsFromTableByListLookup(self.getAvailableCharsets(),lambda x:x.name,wanted_charsets)

    def selectMarkovFile(self,markov_file:str) -> None:
        activateElementsFromTableByListLookup(self.getAvailableMarkovFiles(),lambda x:x.name,[markov_file])

    def getSelectedMarkovMode(self) -> MarkovMode:
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
                raise Exception('Invalid state of Markov-mode radio button (either no mode is selected or more than one mode is selected at once).')

    def selectMarkovMode(self, markov_mode:MarkovMode) -> None:
        match markov_mode:
            case MarkovMode.MARKOV_DISABLED:
                obstructedClickWorkaround(self.driver,self.__markov_disabled_radio_button)
            case MarkovMode.MARKOV_2D:
                obstructedClickWorkaround(self.driver,self.__2D_markov_radio_button)
            case MarkovMode.MARKOV_3D:
                obstructedClickWorkaround(self.driver,self.__3D_markov_radio_button)

    def setMarkovThresholdValue(self,threshold:int) -> None:
        self.__markov_threshold_input.clear()
        self.__markov_threshold_input.send_keys(str(threshold))

    def setMaskValue(self,mask_value:str,index:int) -> None:
        self.__get_mask_input_field(index).clear()
        self.__get_mask_input_field(index).send_keys(mask_value)

    def addMask(self) -> None:
        self.__add_mask_button.click()

    def removeMask(self,index:int) -> None:
        self.__get_mask_remove_button(index).click()

    def getAllInputMasks(self) -> List[str]:
        inputMasks = list()
        for i in itertools.count():
            try:
                inputMasks.append(self.__get_mask_input_field(i).get_attribute('value'))
            except NoSuchElementException:
                break
        return inputMasks

    def setMasksFromList(self,masks:List[str]) -> None:
        numberOfAlreadyInputMasks = len(self.getAllInputMasks())
        for i in range(numberOfAlreadyInputMasks-1,0,-1): #Removes masks in reverser order; from top to bottom in the UI.
            self.removeMask(i)
        for i, mask in zip(itertools.count(), masks):
            if i > 0:
                self.addMask()
            self.setMaskValue(mask,i)
            self._click_away()

