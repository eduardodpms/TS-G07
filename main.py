from src.core import TestSuite
from src.test_maker import test_maker
import json


############# Variáveis de Ambiente #############
service_driver = '/usr/bin/geckodriver'
web_driver = 'Firefox'
tests_json = 'tests/tests.json'
address = 'http://localhost:3000/'
create_tests_mode = False


############# Variáveis de Login #############
logged = True # Se já está logado
user = 'user@user.com'
password = 'password'


############# Execução da suite de testes #############
if create_tests_mode:
    test_maker(tests_json)
else:
    with open(tests_json, 'r') as f:
        tests = json.load(f)

    suite = TestSuite(service_driver, web_driver, logged, address, tests, headless=False)
