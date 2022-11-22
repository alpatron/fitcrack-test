import unittest
from selenium import webdriver
from PageObjects import LoginPage, JobCreationPage

PREFIX = 'http://192.168.56.2:81'

class jobCreationTest(unittest.TestCase):
    def setUp(self):
        self.driver =  webdriver.Firefox()
        #self.driver.implicitly_wait(30)

    def test(self):
        loginPage = LoginPage(self.driver,no_ensure_loaded=True)
        loginPage.navigate(PREFIX)
        loginPage.ensure_loaded()

        sidebar, dashboard = loginPage.login('fitcrack','FITCRACK')
        
        jobCreationPage = sidebar.goto_create_job()
        jobCreationPage.setJobName('A fun job for the whole family!')
        
        inputSettings = jobCreationPage.openInputSettings()
        inputSettings.selectHashTypeExactly("md5")
        inputSettings.inputHashesManually(
            ['718a39dfd0aa7a0acb662a8997aea285',
             'f30aa7a662c728b7407c54ae6bfd27d1']
        )

        attackSettings = jobCreationPage.openAttackSettings()
        dictionarySettings = attackSettings.chooseDictionaryMode()

        dictionaries = dictionarySettings.getAvailableDictionaries()
        
        dictionaries[0].selected = True

        jobCreationPage.createJob()

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()