import pytest
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

# BMO login ekranı ingilizce diline çevirme testi.
class Test_bmo:
    def setup_method(self):
        self.driver=webdriver.Chrome(ChromeDriverManager().install())

    def test_bmo(self):
        expected_result ="I forgot my password"
        self.driver.get("https://uye.bmo.org.tr/#!/login")
        self.driver.maximize_window()
        sleep(2)
        languageBtn = self.driver.find_element(By.XPATH,"/html/body/ui-view/login/div/div/div[2]/div/form/div[5]/div/select")
        languageBtn.click()
        sleep(2)
        enBtn= self.driver.find_element(By.XPATH,"/html/body/ui-view/login/div/div/div[2]/div/form/div[5]/div/select/option[2]")
        enBtn.click()
        sleep(5)
        requestPassword=self.driver.find_element(By.XPATH,"/html/body/ui-view/login/div/div/div[2]/div/form/div[4]/a")
        assert requestPassword.text.strip() == expected_result

    def teardown_method(self):
        self.driver.quit()

# BMO sitesine login olurken geçersiz username ve/veya password girildiği durumda
# vermesi gereken "T.C. Kimlik Numarası/Sicil No ve/veya Parolanız Yanlıştır"
# hata mesajının kontrolü.
class Test_bmoLoginAlert:
    def setup_method(self):
        self.driver=webdriver.Chrome(ChromeDriverManager().install())
    
    @pytest.mark.parametrize("username,password",[("123456789101112","osman3"),("abcdabcdabcd","osman3")])
    def test_invalid_login(self,username,password):
        expected_message = "T.C. Kimlik Numarası/Sicil No ve/veya Parolanız Yanlıştır"
        self.driver.get("https://uye.bmo.org.tr/#!/login")
        WebDriverWait(self.driver,10).until(expected_conditions.visibility_of_element_located((By.ID,"username")))
        usernameInput = self.driver.find_element(By.ID,"username")
        usernameInput.send_keys(username)
        sleep(2)
        WebDriverWait(self.driver,5).until(expected_conditions.visibility_of_element_located((By.ID,"password")))
        passwordInput = self.driver.find_element(By.ID,"password")
        passwordInput.send_keys(password)
        sleep(2)
        loginBtn = self.driver.find_element(By.XPATH,"/html/body/ui-view/login/div/div/div[2]/div/form/div[3]/button")
        loginBtn.click()
        sleep(2)
        WebDriverWait(self.driver,5).until(expected_conditions.visibility_of_element_located((By.XPATH,"/html/body/ui-view/login/div/div/div[2]/div/form/div[2]/div[1]/span")))
        errLabel = self.driver.find_element(By.XPATH,"/html/body/ui-view/login/div/div/div[2]/div/form/div[2]/div[1]/span")
        assert errLabel.text.strip() == expected_message
    
    def teardown_method(self):
        self.driver.quit()

# Türk Telekom sitesine login olurken phoneNumber ve/veya password girdi alanları
# boş bırakıldığı durumda "Bu alanın doldurulması zorunludur" uyarı mesajının kontrolü.
class Test_tt:
    def setup_method(self):
        self.driver=webdriver.Chrome(ChromeDriverManager().install())

    def test_empty(self):
        expected_result ="Bu alanın doldurulması zorunludur"
        self.driver.get("https://onlineislemler.turktelekom.com.tr/")
        phoneNumber = self.driver.find_element(By.XPATH,"//*[@id='mobilHomeLogin']/form/div[2]/div/div/input")
        phoneNumber.click()
        sleep(2)
        password = self.driver.find_element(By.XPATH,"//*[@id='mobilHomeLogin']/form/div[3]/div/div/input")
        password.click()
        sleep(2)
        phoneNumber = self.driver.find_element(By.XPATH,"//*[@id='mobilHomeLogin']/form/div[2]/div/div/input")
        phoneNumber.click()
        sleep(2)
        errLabel = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div/div/div[1]/div[1]/div[2]/form/div[2]/div/span/span")
        assert errLabel.text.strip() == expected_result
        sleep(2)
    
    def teardown_method(self):
        self.driver.quit()
