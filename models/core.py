import json
import time
import undetected_chromedriver
import numpy as np

from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth


class Core(ABC):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.binary_location = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'

    @abstractmethod
    def check_for_multiple_pages(self) -> bool:
        pass

    @abstractmethod
    def mine_links(self) -> None:
        pass

    @abstractmethod
    def get_links_to_papers(self) -> None:
        pass

    @abstractmethod
    def construct_full_link(self) -> str:
        pass

    @abstractmethod
    def create_query_text(self) -> str:
        pass

    @staticmethod
    def encode_search_terms_into_query(keywords: str, scrapper: str) -> str:
        """
        encode user given search terms into URL string

        Parameters
        ----------
        scrapper: str {'ACM', 'SCIDIR'}
            use different encoding method based on which
            scrapper being use

        keywords: str
            search terms to create search query

        Returns
        -------

        """
        if scrapper == 'ACM':
            encode = keywords.replace(' ', "+")
            encode = encode.replace(';', "%3B")
            encode = encode.replace(':', "%3A")
            encode = encode.replace(',', "%2C")
            encode = encode.replace('(', "%28")
            encode = encode.replace(')', "%29")

            return encode

        elif scrapper == 'SCIDIR':
            encode = keywords.replace(' ', "%20")
            encode = encode.replace(';', "%3B")
            encode = encode.replace(',', "%2C")

            return encode

        else:
            raise AttributeError('wrong scrapper type.')

    def init_driver(self) -> None:
        """
        initiate web driver and session

        Returns
        -------

        """
        self.driver = undetected_chromedriver.Chrome(chrome_options=self.options,
                                                     executable_path='D:\\chromedriver.exe')

    def close_driver(self) -> None:
        """
        close web driver and session

        Returns
        -------

        """
        self.driver.close()

    def post_request(self, link) -> None:
        """
        post a request to science direct server

        Parameters
        ----------
        link: str
            URL to make request on

        Returns
        -------

        """
        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        # make request
        self.driver.delete_all_cookies()
        self.driver.get(link)
        time.sleep(abs(np.random.normal(2, 0.4)))

    def to_json(self, path: str) -> None:
        """
        dump links to json file

        Parameters
        ----------
        path: str
            string path for save results (link and additional details)

        Returns
        -------

        """
        with open(path, 'w') as file:
            json.dump(self.links_to_paper, file)
