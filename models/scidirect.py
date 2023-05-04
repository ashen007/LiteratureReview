import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class ScienceDirect:
    options = Options()
    options.binary_location = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'

    def __init__(self, start, end, search_terms):
        self.driver = webdriver.Chrome(chrome_options=self.options,
                                       executable_path='D:\\chromedriver.exe')
        self.origin = "https://www.sciencedirect.com/search"
        self.date_filter = f"?date={start}-{end}"
        self.results_in_a_page = "&show=100"
        self.query_text = self.encode_search_terms_into_query(search_terms)
        self.article_type = "&articleTypes=FLA"

        self.driver.get(self.construct_full_link())
        time.sleep(3)

    def construct_full_link(self):
        return ''.join([self.origin,
                        self.date_filter,
                        self.query_text,
                        self.results_in_a_page,
                        self.article_type])

    @staticmethod
    def encode_search_terms_into_query(keywords):
        encode = keywords.replace(' ', "%20")
        encode = encode.replace(';', "%3B")
        encode = encode.replace(',', "%2C")

        return f"&qs={encode}"

    def get_total_result_count(self):
        tot_results = int(self.driver.find_element(By.CLASS_NAME,
                                                   value="search-body-results-text").text.split(' ')[0])

        return tot_results

    def get_links_list(self):
        return

    def to_csv(self):
        return
