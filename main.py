from src.core import TestSuite
from src.test_maker import test_maker
import json


address = 'http://localhost:3000/'
service_driver = '/usr/bin/geckodriver'
web_driver = 'Firefox'
tests_json = 'tests/tests.json'
create_tests_mode = False


if create_tests_mode:
    test_maker(tests_json)
else:
    with open(tests_json, 'r') as f:
        tests = json.load(f)

    suite = TestSuite(service_driver, web_driver, address, tests, headless=False)
