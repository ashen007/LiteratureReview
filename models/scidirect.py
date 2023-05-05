import time
import json
import numpy as np
import undetected_chromedriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth


class ScienceDirect:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.binary_location = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'

    def __init__(self, start, end, search_terms):
        self.driver = None
        self.page_count = None
        self.links_to_paper = {}
        self.origin = "https://www.sciencedirect.com/search"
        self.date_filter = f"?date={start}-{end}"
        self.results_in_a_page = "&show=100"
        self.offset = "&offset=0"
        self.query_text = self.encode_search_terms_into_query(search_terms)
        self.article_type = "&articleTypes=FLA"

    @staticmethod
    def encode_search_terms_into_query(keywords):
        encode = keywords.replace(' ', "%20")
        encode = encode.replace(';', "%3B")
        encode = encode.replace(',', "%2C")

        return f"&qs={encode}"

    def construct_full_link(self):
        return ''.join([self.origin,
                        self.date_filter,
                        self.query_text,
                        self.results_in_a_page,
                        self.offset,
                        self.article_type])

    def init_driver(self):
        self.driver = undetected_chromedriver.Chrome(chrome_options=self.options,
                                                     executable_path='D:\\chromedriver.exe')

    def close_driver(self):
        self.driver.close()

    def post_request(self, link):
        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        # make request
        self.driver.get(link)
        time.sleep(np.random.normal(2, 0.4))

    def check_for_multiple_pages(self):
        link = self.construct_full_link()
        self.init_driver()
        self.post_request(link)

        tot_results = int(self.driver.find_element(By.CLASS_NAME,
                                                   value="search-body-results-text").text.split(' ')[0])
        self.page_count = int(np.round(tot_results / 100))

        time.sleep(2)
        self.close_driver()

        return True if tot_results / 100 > 1 else False

    def mine_links(self):
        for title, article in zip(self.driver.find_elements(By.CLASS_NAME, value="result-list-title-link"),
                                  self.driver.find_elements(By.CLASS_NAME, value="article-type")):
            self.links_to_paper[title.get_attribute('id')] = [title.get_attribute('href'), article.text]

        time.sleep(np.random.uniform(2, 4))

    def get_links_to_papers(self):
        if self.check_for_multiple_pages():
            for i in range(self.page_count):
                self.offset = f"&offset={100 * i}"
                self.init_driver()
                self.post_request(self.construct_full_link())
                self.mine_links()

                print(f'reading page: {i+1} from {self.page_count}', end='\r')

                self.close_driver()

        else:
            self.mine_links()
            self.close_driver()

    def to_csv(self, path):
        with open(path, 'w') as file:
            json.dump(self.links_to_paper, file)
