import pytest

from src.utils import *
from pytest import raises


def test_is_config_exists(file_name='x.json'):
    with raises(FileNotFoundError):
        read_json(file_name)


def test_whether_config_empty(file_name='./empty.json'):
    config = read_json(file_name)

    with raises(ConfigurationError):
        validate(config)


def test_config_file():
    config = read_json('../config.json')
    validate(config)


def test_able_to_identify_bad_config():
    config = read_json('./bad.json')

    with raises(ConfigurationError):
        validate(config)

    with raises(ConfigurationError):
        obj = {
            "BINARY_LOCATION": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "EXECUTABLE_PATH": "D:\\chromedriver.exe",
            "ACM": {
                "search_term": "",
                "link_file_save_to": "./temp/acm_search_term.json",
                "abs_file_save_to": "./abs/acm_search_term.json",
                "use_batches": True,
                "batch_size": 8,
                "keep_link_file": True
            },
            "SCIDIR": {
            }
        }

        validate(obj)
