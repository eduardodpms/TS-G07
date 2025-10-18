from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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


    def post(self, title, body, source, sponsored):

        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='Publicar novo conteúdo']"))
        ).click()

        post = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Publicar']"))
        )

        self.driver.find_element(By.ID, "title").send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
        self.driver.find_element(By.CLASS_NAME, "CodeMirror-code").send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
        self.driver.find_element(By.ID, "source_url").send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)

        self.driver.find_element(By.ID, "title").send_keys(title)
        self.driver.find_element(By.CLASS_NAME, "CodeMirror-code").send_keys(body)
        self.driver.find_element(By.ID, "source_url").send_keys(source)

        if (sponsored) ^ bool(self.driver.find_elements(By.XPATH, "//input[@name='isSponsoredContent' and @aria-checked='true']")):
            self.driver.find_element(By.XPATH, "//input[@name='isSponsoredContent']").click()

        post.click()
        self.driver.find_element(By.XPATH, "//span[text()='Publicar']").click()


    def run(self):
        n, m = 0, len(self.tests)

        try:
            self.driver.get(self.address)
            self.login(self.user, self.password)
            print(f"Login successful. Starting test suite...\n{'-'*26}")
        except Exception as e:
            print(f"Login failed:\n{e}")
            self.driver.quit()
            return

        for test in self.tests:

            print(f"> Running Test '{test['id']}'")

            self.wait.until(
                EC.visibility_of_element_located((By.ID, "header"))
            )

            try:
                self.post(test['title'], test['body'], test['source'], test['sponsored'])
            except Exception as e:
                print(f"> Failed to publish post '{test['id']}':\n{e}")
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

                n += 1
                print(f"> Passed Test '{test['id']}' ({n}/{m})\n{'-'*26}")
            except Exception:
                print(f"> Failed Test '{test['id']}' ({n}/{m})\n{'-'*26}")

            #time.sleep(5)

        print(f"Test suite finished: {n}/{m} passed.")
        self.driver.close()
