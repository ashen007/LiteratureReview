import json
import os.path
from selenium.webdriver.support.ui import WebDriverWait


class ConfigurationError(Exception):
    """
    raise when scrapper configuration misses
    expected key or keys
    """

    def __int__(self, exp_keys: list):
        self.exp_keys = exp_keys

    def __repr__(self):
        return f"{' '.join(self.exp_keys)} one or more keys missing from those."


def clean_cookies_and_caches(driver):
    # first falls check
    if driver is not None:
        driver.delete_all_cookies()

    # step 2
    # method 1
    driver.execute_script('window.localStorage.clear()')

    # method 2
    driver.execute_script('window.sessionStorage.clear()')


def read_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


def validate(obj: dict):
    if obj == {}:
        raise ConfigurationError()

    scrappers = {'IEEE', 'ACM', 'SCIDIR'}.intersection(set(obj.keys()))
    if not obj.get('BINARY_LOCATION', False):
        raise ConfigurationError()

    if not obj.get('EXECUTABLE_PATH', False):
        raise ConfigurationError()

    assert len(scrappers) != 0

    print(f"detected scrappers: {scrappers}")
    print('=' * 25)

    validate_scrapper_keys(obj, scrappers)

    return True


def validate_scrapper_keys(obj: dict, detected: set):
    expected_keys = ['search_term', 'link_file_save_to',
                     'abs_file_save_to', 'use_batches',
                     'batch_size', 'keep_link_file']
    for s in detected:
        if list(obj[s].keys()) != expected_keys:
            raise ConfigurationError(expected_keys)
