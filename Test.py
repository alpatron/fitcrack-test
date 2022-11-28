import unittest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from page_object.LoginPage import LoginPage

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
        inputSettings.selectHashTypeExactly("sha1")
        inputSettings.inputHashesManually(
            ['c0b51c46e4dcde6189e48ec9695fe55efc0ea703', # strawberry
             'c0baf4391defd68bf678f0a5ca2b69f828177ddf', # str@wberry
             '240794c3cd2f7c5be0c58340e2dd33a5518b543a', # strawBerry
             'e083612b4a67573e1d46743c39878d44e81916cd', # Amanda
             'e7b66d3af606d05d40d89bdd18e437a1be28b625'  # Amanda13
            ] 
        )

        attackSettings = jobCreationPage.openAttackSettings()
        dictionarySettings = attackSettings.chooseDictionaryMode()

        dictionarySettings.selectDictionaries([
            'darkweb2017-top1000.txt'
        ])
        

        jobDetailPage = jobCreationPage.createJob()

        assert jobDetailPage.get_job_state() == 'Ready'

        jobDetailPage.start_job()

        WebDriverWait(self.driver,600).until(lambda _: jobDetailPage.get_job_state() == 'Finished')

        workedOnHashes = jobDetailPage.getHashes()
        crackedHashes = list(filter(lambda x: x[1] != '',workedOnHashes))
        uncrackedHashes = list(filter(lambda x: x[1] == '',workedOnHashes))

        assert len(crackedHashes) == 1
        assert len(uncrackedHashes) == 4

        assert crackedHashes[0][0] == 'c0b51c46e4dcde6189e48ec9695fe55efc0ea703' and crackedHashes[0][1] == 'strawberry'

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()