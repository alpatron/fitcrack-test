from seleniumbase import BaseCase
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import By
from typing import List

class PageObject:
    def __init__(self,sb:BaseCase):
        self.sb = sb

class LoginPage(PageObject):
    URL_PATH = '/login'
    
    USERNAME_FIELD = '#input20'
    PASSWORD_FIELD = '#input23'
    SUBMIT_BUTTON  = 'button[type="submit"]'

    def navigate(self,prefix):
        self.sb.goto(prefix+self.URL_PATH)

    def login(self,username,password):
        self.sb.clear(self.USERNAME_FIELD)
        self.sb.type(self.USERNAME_FIELD,username)
        self.sb.clear(self.PASSWORD_FIELD)
        self.sb.type(self.PASSWORD_FIELD,password)
        self.sb.click(self.SUBMIT_BUTTON)

class Dashboard(PageObject):
    WELCOME_TEXT = 'h1'

class SideBar(PageObject):
    JOBS_BUTTON = '#nav-jobs-tab'
    LIBRARY_BUTTON = '#nav-library-tab'
    SYSTEM_BUTTON = '#nav-system-tab'

    ADD_JOB_BUTTON = 'a[href="/jobs/add"]'

class JobCreation(PageObject):
    NAME_FIELD = '#input-973'

    INPUT_SETTINGS_BUTTON = '#job-step-1'
    ATTACK_SETTINGS_BUTTON = '#job-step-2'
    HOST_ASSIGNMENT_BUTTON = '#job-step-3'
    ADDITIONAL_SETTINGS_BUTTON = '#job-step-4'

    CREATE_BUTTON = {'selector':'//button[text()="Create"]','by':By.XPATH}
    
    def setJobName(self,name:str):
        self.sb.clear(self.NAME_FIELD)
        self.sb.type(name)

    def getJobName(self) -> str:
        jobName : WebElement = self.sb.find_element(self.NAME_FIELD)
        return jobName.getProperty('value')

    def createJob(self):
        self.sb.click(**self.CREATE_BUTTON)

class InputSettings(PageObject):
    MANUAL_ENTRY_BUTTON = '#job-input-mode-manual'
    HASH_FILE_ENTRY_BUTTON = '#job-input-mode-hashlist'
    FILE_EXTRACT_ENTRY_BUTTON = '#job-input-mode-extract'

    HASH_INPUT_FIELD = '#hashes-input textarea'
    HASH_TYPE_SELECTION_INPUT = '#hash-type-select'

    HASH_TYPE_SELECTION_SEARCH_PRIME_CANDIDATE = '#list-263>div:first-child'

    def selectHashTypeExactly(self,hashtype:str):
        self.sb.type(self.HASH_INPUT_FIELD,hashtype)

    def getSelectedHashType(self) -> str:
        hashSelection : WebElement = self.sb.find_element(self.HASH_TYPE_SELECTION_INPUT)
        return hashSelection.getProperty('value')

    def inputHashesManually(self,hashes:List[str]):
        self.sb.clear(self.HASH_INPUT_FIELD)
        self.sb.type(self.HASH_INPUT_FIELD,'\n'.join(hashes))

class AttackSettings(PageObject):
    DICTIONARY_MODE_BUTTON = '#attack-mode-dictionary'
    COMBINATION_MODE_BUTTON = '#attack-mode-combinator'
    BRUTEFORCE_MODE_BUTTON = '#attack-mode-maskattack'
    HYBRID_WORDLIST_AND_MASK_MODE_BUTTON = '#attack-mode-hybridWordlistMask'
    HYBRID_MASK_AND_WORDLIST_MODE_BUTTON = '#attack-mode-hybridMaskWordlist'
    PRINCE_MODE_BUTTON = '#attack-mode-princeAttack'
    PCFG_MODE_BUTTON = '#attack-mode-princeAttack'

    def chooseDictionaryMode(self):
        self.sb.click(self.DICTIONARY_MODE_BUTTON)
        return DictionaryAttackSettings(self.sb)

    def chooseCombinationMode(self):
        self.sb.click(self.COMBINATION_MODE_BUTTON)
        return CombinationAttackSettings(self.sb)

    def chooseBruteforceMode(self):
        self.sb.click(self.BRUTEFORCE_MODE_BUTTON)
        return BruteforceAttackSettings(self.sb)

    def chooseHybridWordlistAndMaskMode(self):
        self.sb.click(self.HYBRID_WORDLIST_AND_MASK_MODE_BUTTON)
        return HybridWordlistAndMaskAttackSettings(self.sb)

    def chooseHybridMaskAndWordlistMode(self):
        self.sb.click(self.HYBRID_MASK_AND_WORDLIST_MODE_BUTTON)
        return HybridMaskAndWordlistAttackSettings(self.sb)

    def choosePrinceMode(self):
        self.sb.click(self.PRINCE_MODE_BUTTON)
        return PrinceAttackSettings(self.sb)

    def choosePCFGMode(self):
        self.sb.click(self.PCFG_MODE_BUTTON)
        return PCFGAttackSettings(self.sb)

class DictionaryAttackSettings(PageObject):
    pass    

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
    
