from django.test import LiveServerTestCase
# from django.test import TestCase
from django.urls import reverse_lazy
# from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# Create your tests here.

class TestLogin(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # cls.selenium = WebDriver(executable_path='/usr/local/bin/chromedriver')
        # cls.selenium = webdriver.Chrome(executable_path = '/usr/local/bin/chromedriver')
        service = Service('/usr/local/bin/chromedriver')
        cls.selenium = webdriver.Chrome(service=service)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        # ログインページを開く
        self.selenium.get('http://localhost:8000' + str(reverse_lazy('account_login')))

        # ログイン
        # username_input = self.selenium.find_element_by_name("login")
        username_input = self.selenium.find_element(By.NAME, "login") #selenium4以降
        username_input.send_keys('example4@example.com')
        # password_input = self.selenium.find_element_by_name("password")
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('Test12345')
        # self.selenium.find_element_by_class_name('btn').click()

        # 要素がクリック可能になるまで待つ
        # login_button = WebDriverWait(self.selenium, 10).until(
        #     EC.element_to_be_clickable((By.CLASS_NAME, 'btn'))
        # )
        # login_button.click()

        # JavaScriptでクリック
        login_button = self.selenium.find_element(By.CLASS_NAME, 'btn')
        self.selenium.execute_script("arguments[0].click();", login_button)

        # self.selenium.find_element(By.CLASS_NAME, 'btn').click()

        # ページタイトルの検証
        # self.assertEqual('日記一覧 | Private Diary', self.selenium.title)
        self.assertEqual('Log In | Private Diary', self.selenium.title)
