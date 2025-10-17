from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestSuite():
    def __init__(self, service_driver, web_driver, address, tests, headless=False, wait=4, user=None, password=None):
        self.address = address
        self.tests = tests

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
        self.driver.get(address)

        
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "header"))
        )

        if self.driver.find_elements(By.XPATH, "//header[@id='header']//a[text()='Login']"):
            try:
                self.login(user, password)
            except Exception as e:
                print(f"Login failed:\n{e}")
                self.driver.quit()
                return

        if(input("Start tests? (y/n): ").lower() == 'y'):
            self.run()


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




    def run(self):
        pass