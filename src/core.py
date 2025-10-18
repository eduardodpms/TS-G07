from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class TestSuite():
    def __init__(self, service_driver, web_driver, address, tests, headless=False, wait=4, user=None, password=None):
        self.address = address
        self.tests = tests
        self.user = user
        self.password = password

        if hasattr(webdriver, web_driver):
            self.service = getattr(webdriver, web_driver.lower())
            self.service = self.service.service.Service(service_driver)

            self.options = getattr(webdriver, web_driver.lower())
            self.options = self.options.options.Options()
            if headless:
                self.options.add_argument("--headless") # executa sem abrir janela

            self.driver = getattr(webdriver, web_driver)(self.options, self.service)
        else:
            raise ValueError("Web driver not supported")

        self.wait = WebDriverWait(self.driver, wait)


    def login(self, user, password):

        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//header[@id='header']//a[text()='Login']"))
        ).click()

        login = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Login']"))
        )

        self.driver.find_element(By.ID, "email").send_keys(user)
        self.driver.find_element(By.ID, "password").send_keys(password)

        login.click()

        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Abrir o menu']"))
        )

        print("Login successful.")


    def post(self, title, body, source, sponsored):

        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='Publicar novo conteúdo']"))
        ).click()

        post = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Publicar']"))
        )

        self.driver.find_element(By.ID, "title").send_keys(title)
        self.driver.find_element(By.CLASS_NAME, "CodeMirror-code").send_keys(body)
        self.driver.find_element(By.ID, "source_url").send_keys(source)
        if sponsored:
            self.driver.find_element(By.XPATH, "//input[@name='isSponsoredContent']").click()

        post.click()
        self.driver.find_element(By.XPATH, "//span[text()='Publicar']").click()


    def run(self):
        n, m = 0, len(self.tests)

        try:
            self.driver.get(self.address)
            self.login(self.user, self.password)
        except Exception as e:
            print(f"Login failed:\n{e}")
            self.driver.quit()
            return

        for test in self.tests:

            print(f"Running test with ID = '{test['id']}'")

            self.wait.until(
                EC.visibility_of_element_located((By.ID, "header"))
            )

            try:
                self.post(test['title'], test['body'], test['source'], test['sponsored'])
            except Exception as e:
                print(f"Failed to publish post '{test['id']}':\n{e}")
                return
            
            try:
                if not test['expected']:
                    self.wait.until(
                        EC.visibility_of_element_located((By.XPATH, "//button[@data-size='small' and @data-variant='default']"))
                    )
                    self.driver.find_element(By.XPATH, "//button[@data-size='small' and @data-variant='default']").click()
                    self.driver.find_element(By.XPATH, "//span[text()='Apagar']").click()
                    self.driver.find_element(By.XPATH, "//span[text()='Sim']").click()
                else:
                    self.driver.find_element(By.XPATH, f"//*[contains(text(), '{test['expected']}')]")
                    self.driver.find_element(By.XPATH, "//div[text()='TabNews']").click()

                n += 1
                print(f"Test '{test['id']}' passed ({n}/{m}).\n")
            except Exception as e:
                print(f"Test '{test['id']}' failed ({n}/{m}).\n")

            time.sleep(3)
        #self.driver.quit()
