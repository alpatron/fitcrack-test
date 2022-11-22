from __future__ import annotations

from selenium.webdriver.common.by import By
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement

from page_object.PageObject import PageObject
from page_object.DictionaryAttackSettings import DictionaryAttackSettings
from page_object.HybridMaskAndWordlistAttackSettings import HybridMaskAndWordlistAttackSettings
from page_object.HybridWordlistAndMaskAttackSettings import HybridWordlistAndMaskAttackSettings
from page_object.BruteforceAttackSettings import BruteforceAttackSettings
from page_object.CombinationAttackSettings import CombinationAttackSettings
from page_object.PrinceAttackSettings import PrinceAttackSettings
from page_object.PCFGAttackSettings import PCFGAttackSettings

class AttackSettings(PageObject):
    @property
    def dictionary_mode_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'attack-mode-dictionary')
    @property
    def combination_mode_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'attack-mode-combinator')
    @property
    def bruteforce_mode_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'attack-mode-maskattack')
    @property
    def hybrid_wordlist_and_mask_mode_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'attack-mode-hybridwordlistmask')
    @property
    def hybrid_mask_and_wordlist_mode_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'attack-mode-hybridmaskwordlist')
    @property
    def prince_mode_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'attack-mode-princeattack')
    @property
    def pcfg_mode_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'attack-mode-princeattack')

    def chooseDictionaryMode(self) -> DictionaryAttackSettings:
        self.dictionary_mode_button.click()
        return DictionaryAttackSettings(self.driver)

    def chooseCombinationMode(self) -> CombinationAttackSettings:
        self.combination_mode_button.click()
        return CombinationAttackSettings(self.driver)

    def chooseBruteforceMode(self) -> BruteforceAttackSettings:
        self.bruteforce_mode_button.click()
        return BruteforceAttackSettings(self.driver)

    def chooseHybridWordlistAndMaskMode(self) -> HybridWordlistAndMaskAttackSettings:
        self.hybrid_wordlist_and_mask_mode_button.click()
        return HybridWordlistAndMaskAttackSettings(self.driver)

    def chooseHybridMaskAndWordlistMode(self) -> HybridMaskAndWordlistAttackSettings:
        self.hybrid_mask_and_wordlist_mode_button.click()
        return HybridMaskAndWordlistAttackSettings(self.driver)

    def choosePrinceMode(self) -> PrinceAttackSettings:
        self.prince_mode_button.click()
        return PrinceAttackSettings(self.driver)

    def choosePCFGMode(self) -> PCFGAttackSettings:
        self.pcfg_mode_button.click()
        return PCFGAttackSettings(self.driver)