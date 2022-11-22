from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from typing import List, TYPE_CHECKING
from selenium.common.exceptions import JavascriptException, NoSuchElementException, TimeoutException
if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement

class PageObject:
    def __init__(self,driver:WebDriver,no_ensure_loaded=False):
        self.driver = driver
        if not no_ensure_loaded:
            self.ensure_loaded()

    def ensure_loaded(self):
        pass

class JobDetailPage(PageObject):
    
    @property
    def __start_button(self):
        return self.driver.find_element(By.XPATH,'//span[text()[contains(.,"start")]]')

class DictionarySelection(PageObject):
    def __init__(self,driver:WebDriver,element:WebElement):
        super().__init__(driver)
        self.__element = element

    @property
    def __name_field(self) -> WebElement:
        return self.__element.find_element(By.CSS_SELECTOR,'td:nth-child(2) a')

    @property
    def __keyspace_field(self) -> WebElement:
        return self.__element.find_element(By.CSS_SELECTOR,'td:nth-child(3)')

    @property
    def __selection_checkbox(self) -> WebElement:
        return self.__element.find_element(By.CSS_SELECTOR, 'td:nth-child(1) i')


    #Dunno if I want to use properties for this nonsense.
    @property
    def name(self) -> str:
        return self.__name_field.text

    @property
    def keyspace(self) -> str:
        return self.__keyspace_field.text

    @property
    def selected(self) -> bool:
        checkboxClasses = self.__selection_checkbox.get_attribute('class')
        if 'mdi-checkbox-blank-outline' in checkboxClasses and not 'mdi-checkbox-marked' in checkboxClasses:
            return False
        elif 'mdi-checkbox-marked' in checkboxClasses and not 'mdi-checkbox-blank-outline' in checkboxClasses:
            return True
        else:
            raise Exception('The selection state of a checkbox could not be determined. This may indicate a brokem page object.')
    
    @selected.setter
    def selected(self,newState:bool) -> None:
        if newState == self.selected:
            return
        #We use the low-level API instead of regular element.click() because the way the app is coded
        #a ripple effect "obstructs" the checkbox, causing regular element.click() to fail saying the element's non-interactable.
        ActionChains(self.driver).click(self.__selection_checkbox).perform() 
    
class DictionaryAttackSettings(PageObject):
    def ensure_loaded(self):
        '''Waits until some dictionaries are available in the dictionary selection until a timeout.
        If the dictonary selector is still blank after the timeout, we assume that that is correct,
        and that there are indeed no dictionaries and proceed.
        Even if it succeeds and sees that dictionaries are loaded, we wait for two seconds to ensure
        that vuejs actually properly displays the elements.
        '''
        try:
            WebDriverWait(self.driver,30).until(lambda _: len(self.getAvailableDictionaries()) != 0)
            ActionChains(self.driver).pause(2).perform()
        except TimeoutError:
            pass

    
    @property
    def __dictionary_selection_table(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'table').below({By.XPATH:'//span[text()[contains(.,"Select dictionary")]]'})  # type: ignore
        )

    @property
    def __rule_file_selection_table(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'table').below({By.XPATH:'//span[text()[contains(.,"Select rule file")]]'})  # type: ignore
        )
    
    def getAvailableDictionaries(self) -> List[DictionarySelection]:
        return [DictionarySelection(self.driver,tableRow) for tableRow in self.__dictionary_selection_table.find_elements(By.CSS_SELECTOR,'tbody tr')]


class CombinationAttackSettings(PageObject):
    pass

class BruteforceAttackSettings(PageObject):
    pass

class HybridWordlistAndMaskAttackSettings(PageObject):
    pass

class HybridMaskAndWordlistAttackSettings(PageObject):
    pass

class PrinceAttackSettings(PageObject):
    pass
    
class PCFGAttackSettings(PageObject):
    pass

class Dashboard(PageObject):
    @property
    def welcome_text(self) -> WebElement:
        return self.driver.find_element(By.TAG_NAME,'h1')

class LoginPage(PageObject):
    URL_PATH = '/login'
    
    def ensure_loaded(self):
        WebDriverWait(self.driver,30,ignored_exceptions={JavascriptException, NoSuchElementException}).until(lambda _:self.username_field)

    @property
    def username_field(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'input').near({By.XPATH:'//label[text()="Username"]'})  # type: ignore
        )

    @property
    def password_field(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'input').near({By.XPATH:'//label[text()="Password"]'})  # type: ignore
        )

    @property
    def submit_button(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR,'button[type="submit"]')

    def navigate(self,prefix:str) -> None:
        self.driver.get(prefix+self.URL_PATH)

    def login(self,username:str,password:str) -> tuple[SideBar,Dashboard]:
        self.username_field.clear()
        self.username_field.send_keys(username)
        self.password_field.clear()
        self.password_field.send_keys(password)
        self.submit_button.click()
        return SideBar(self.driver), Dashboard(self.driver)

class SideBar(PageObject):
    
    def ensure_loaded(self):
        WebDriverWait(self.driver,30).until(lambda _:self.jobs_button)
    
    @property
    def jobs_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'nav-jobs-tab')    
    @property
    def library_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'nav-library-tab')
    @property
    def system_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'nav-system-tab')
    @property
    def add_job_button(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR,'a[href="/jobs/add"]')

    def goto_create_job(self) -> JobCreationPage:
        self.jobs_button.click()
        self.add_job_button.click()
        return JobCreationPage(self.driver)

class InputSettings(PageObject):
    @property
    def __manual_entry_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'job-input-mode-manual')
    @property
    def __hash_file_entry_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'job-input-mode-hashlist')
    @property
    def __file_extract_entry_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'job-input-mode-extract')

    @property
    def __hash_input_field(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR,'#hashes-input textarea')

    @property
    def __hash_type_selection_input(self) -> WebElement:
        return self.driver.find_element(By.ID,'hash-type-select')

    @property
    def __hash_type_selection_list(self) -> WebElement:
        return self.driver.find_element( #todo: replace back with near locator once Selenium accepts my PR
            locate_with(By.CLASS_NAME,'v-list').below(self.__hash_type_selection_input)  # type: ignore
        )

    def selectHashTypeExactly(self,hashtype:str) -> None: #Todo:this ain't really exact, but whateever; will be fixed later
        self.__hash_type_selection_input.click()
        self.__hash_type_selection_input.clear()
        self.__hash_type_selection_input.send_keys(hashtype)
        WebDriverWait(self.driver,30,ignored_exceptions={JavascriptException, NoSuchElementException}).until(lambda _: self.__hash_type_selection_list)
        self.__hash_type_selection_list.find_element(By.CSS_SELECTOR,'div:nth-child(1)').click()

    def getSelectedHashType(self) -> str:
        return self.__hash_input_field.get_attribute('value')

    def inputHashesManually(self,hashes:List[str]):
        self.__manual_entry_button.click()
        self.__hash_input_field.clear()
        self.__hash_input_field.send_keys('\n'.join(hashes))

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

class JobCreationPage(PageObject):
    def ensure_loaded(self):
        WebDriverWait(self.driver,30,ignored_exceptions={JavascriptException, NoSuchElementException}).until(lambda _: self.__name_field)
    
    @property
    def __name_field(self) -> WebElement:
        return self.driver.find_element(
            locate_with(By.TAG_NAME,'input').near({By.XPATH:'//label[text()="Name"]'})  # type: ignore
        )
    @property
    def __input_settings_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'job-step-1')
    @property
    def __attack_settings_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'job-step-2')
    @property
    def __host_assignment_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'job-step-3')
    @property
    def __additional_settings_button(self) -> WebElement:
        return self.driver.find_element(By.ID,'job-step-4')
    @property
    def __create_button(self) -> WebElement:
        return self.driver.find_element(By.XPATH,'//button[text()="Create"]')
    
    def setJobName(self,name:str) -> None:
        self.__name_field.clear()
        self.__name_field.send_keys(name)

    def getJobName(self) -> str:
        return self.__name_field.get_attribute('value')

    def createJob(self) -> None:
        self.__create_button.click()

    def openInputSettings(self) -> InputSettings:
        self.__input_settings_button.click()
        return InputSettings(self.driver)

    def openAttackSettings(self) -> AttackSettings:
        self.__attack_settings_button.click()
        return AttackSettings(self.driver)

