from selenium import webdriver


class TestSuite():
    def __init__(self, service_driver, web_driver, logged, address, tests, headless=False, user=None, password=None):
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

    
        #self.driver.get(address)
        if not logged:
            self.login(user, password)
        #driver.quit()

    def login(self, user, password):
        pass

    def run(self):
        pass