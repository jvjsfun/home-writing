from django.test import LiveServerTestCase
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import time


class AccountTestCase(LiveServerTestCase):

    BASE_URL = 'https://www.prontopro.ch'
    LOGIN = BASE_URL + '/de/login'
    ADMIN_URL = BASE_URL + '/admin'
    PROTECTED_PAGE = ADMIN_URL + '/seo/writer/landingPage/snippet/next'

    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(AccountTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(AccountTestCase, self).tearDown()

    def test_register(self):
        selenium = self.selenium
        #selenium = webdriver.Firefox()
        #PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
        #DRIVER_BIN = os.path.join(sys.argv[2])
        #driver = webdriver.Chrome(executable_path = DRIVER_BIN)
        selenium.get(self.LOGIN)
        input_mail = selenium.find_element_by_id("email")
        input_mail.send_keys('lorenzo.writing@gmail.com')
        input_pwd = selenium.find_element_by_id("password")
        input_pwd.send_keys('Lo1402')
        form = selenium.find_element_by_xpath(
            '/html/body/div/div/div[3]/div[3]/div/div/div[1]/div/div[1]/div/form')
        form.submit()
        time.sleep(5)  # import ipdb; ipdb.set_trace()
        selenium.get(self.PROTECTED_PAGE)
        phpsessid = selenium.get_cookie('PHPSESSID')['value']
        assert phpsessid is not None
        selenium.close()
        # check the returned result
        assert 'Check your email' in selenium.page_source
