from src.core import TestSuite
from src.test_maker import test_maker
import json


############# Variáveis de Ambiente #############
service_driver = '/usr/bin/geckodriver'
web_driver = 'Firefox'
tests_json = 'tests/tests.json'
address = 'http://localhost:3000/'
headless = False # Executa os testes sem abrir interface gráfica
create_tests_mode = False


############# Variáveis de Login #############
user = 'user@user.com'
password = 'password'


############# Execução do sistema #############
if create_tests_mode:
    test_maker(tests_json)
else:
    with open(tests_json, 'r') as f:
        tests = json.load(f)

    suite = TestSuite(service_driver, web_driver,
                      address, tests, headless=headless,
                      user=user, password=password)
    
    suite.run()
