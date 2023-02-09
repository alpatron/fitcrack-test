"""Page object representing attack settings on the Add Job page.
Exports single class--the aforementioned page object.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains

from page_object.page_object import PageObject
from page_object.dictionary_attack_settings import DictionaryAttackSettings
from page_object.hybrid_attack_settings import HybridAttackSettings
from page_object.brute_force_settings import BruteForceAttackSettings
from page_object.combination_attack_settings import CombinationAttackSettings
from page_object.prince_attack_settings import PRINCEAttackSettings
from page_object.pcfg_attack_settings import PCFGAttackSettings

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


class AttackSettings(PageObject):
    """Represents the Attack settings (step 2) on the Add Job page in Webadmin."""

    def ensure_loaded(self):
        WebDriverWait(self.driver,30).until(lambda _: self.__dictionary_mode_button.is_displayed)
        ActionChains(self.driver).pause(2).perform()
        #Wait for 2 seconds to make sure vuejs animation is over

    @property
    def __dictionary_mode_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'attack-mode-dictionary')
    @property
    def __combination_mode_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'attack-mode-combinator')
    @property
    def __bruteforce_mode_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'attack-mode-maskattack')
    @property
    def __hybrid_wordlist_and_mask_mode_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'attack-mode-hybridWordlistMask')
    @property
    def __hybrid_mask_and_wordlist_mode_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'attack-mode-hybridMaskWordlist')
    @property
    def __prince_mode_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'attack-mode-princeAttack')
    @property
    def __pcfg_mode_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'attack-mode-pcfgAttack')

    def choose_dictionary_mode(self) -> DictionaryAttackSettings:
        """Selects the dictionary attack mode and returns the page object representing the
        dictionary-attack settings panel. The AttackSettings object remains useable.
        """
        self.__dictionary_mode_button.click()
        return DictionaryAttackSettings(self.driver)

    def choose_combination_mode(self) -> CombinationAttackSettings:
        """Selects the combination attack mode and returns the page object representing the
        combination-attack settings panel. The AttackSettings object remains useable.
        """
        self.__combination_mode_button.click()
        return CombinationAttackSettings(self.driver)

    def choose_bruteforce_mode(self) -> BruteForceAttackSettings:
        """Selects the brute-force attack mode and returns the page object representing the
        brute-force-attack settings panel. The AttackSettings object remains useable.
        """
        self.__bruteforce_mode_button.click()
        return BruteForceAttackSettings(self.driver)

    def choose_hybrid_wordlist_and_maks_mode(self) -> HybridAttackSettings:
        """Selects the hybrid wordlist-and-mask attack mode and returns the page object
        representing the hybrid-wordlist-and-mask-attack settings panel. Do note that both
        hybrid attack modes use the same HybridAttackSettings object; this is by design.
        The AttackSettings object remains useable.
        """
        self.__hybrid_wordlist_and_mask_mode_button.click()
        return HybridAttackSettings(self.driver)

    def choose_hybrid_mask_and_wordlist_mode(self) -> HybridAttackSettings:
        """Selects the hybrid mask-and-wordlist attack mode and returns the page object
        representing the hybrid-mask-and-wordlist-attack settings panel.Do note that both
        hybrid attack modes use the same HybridAttackSettings object; this is by design.
        The AttackSettings object remains useable.
        """
        self.__hybrid_mask_and_wordlist_mode_button.click()
        return HybridAttackSettings(self.driver)

    def choose_prince_mode(self) -> PRINCEAttackSettings:
        """Selects the PRINCE attack mode and returns the page object representing the
        PRINCE-attack settings panel. The AttackSettings object remains useable.
        """
        self.__prince_mode_button.click()
        return PRINCEAttackSettings(self.driver)

    def choose_pcfg_mode(self) -> PCFGAttackSettings:
        """Selects the PCFG attack mode and returns the page object representing the
        PCFG-attack settings panel. The AttackSettings object remains useable.
        """
        self.__pcfg_mode_button.click()
        return PCFGAttackSettings(self.driver)
