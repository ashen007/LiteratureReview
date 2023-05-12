import time
import json
import numpy as np
import undetected_chromedriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth


class ScienceDirect:
    """
    Parameters
    ----------
    start: int
        start year of the date range filter

    end: int
        end year of the date range filter

    search_terms: str
        string of search terms (it can be comma seperated or semicolon
        seperated string)

    Attributes
    ----------
    driver: undetected_chromedriver.Chrome
        web driver for selenium

    page_count: int
        number of pages in search results

    links_to_paper: dict
        mined links and additional details for results

    origin: str
        origin of science direct advanced search url

    date_filter: str
        date range to filter search results

    results_in_a_page: str
        number of records should show tin single page

    offset: str
        number of records should go forward for next page
        in search results

    query_text: str
        encoded search query string to apply in URL

    article_type: str
        science direct article type category indicator

    Methods
    -------
    encode_search_terms_into_query:
        encode user given search terms into URL string

    construct_full_link:
        create full link to make request from server

    init_driver:
        initiate web driver and session

    close_driver:
        close web driver and session

    post_request:
        post a request to science direct server

    check_for_multiple_pages:
        check weather search results contains multiple pages
        in results

    mine_links:
        get links to each search result (for each individual paper)

    get_links_to_papers:
        create paper link list

    to_json:
        dump results into json

    """

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.binary_location = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'

    def __init__(self, start: int, end: int, search_terms: str):
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
    def encode_search_terms_into_query(keywords: str) -> str:
        """
        encode user given search terms into URL string

        Parameters
        ----------
        keywords: str
            search terms to create search query

        Returns
        -------

        """
        encode = keywords.replace(' ', "%20")
        encode = encode.replace(';', "%3B")
        encode = encode.replace(',', "%2C")

        return f"&qs={encode}"

    def construct_full_link(self) -> str:
        """
        create full link to make request from server

        Returns
        -------

        """
        return ''.join([self.origin,
                        self.date_filter,
                        self.query_text,
                        self.results_in_a_page,
                        self.offset,
                        self.article_type])

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

    def post_request(self, link: str) -> None:
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
        time.sleep(np.random.normal(2, 0.4))

    def check_for_multiple_pages(self) -> bool:
        """
        check weather search results contains multiple pages
        in results

        Returns
        -------

        """
        link = self.construct_full_link()
        self.init_driver()
        self.post_request(link)

        tot_results = int(self.driver.find_element(By.CLASS_NAME,
                                                   value="search-body-results-text").text.split(' ')[0])
        self.page_count = int(np.round(tot_results / 100))

        self.close_driver()

        return True if self.page_count > 1 else False

    def mine_links(self) -> None:
        """
        get links to each search result (for each individual paper)

        Returns
        -------

        """
        for title, article in zip(self.driver.find_elements(By.CLASS_NAME, value="result-list-title-link"),
                                  self.driver.find_elements(By.CLASS_NAME, value="article-type")):
            self.links_to_paper[title.get_attribute('id')] = [title.text,
                                                              title.get_attribute('href'),
                                                              article.text]

        time.sleep(np.random.uniform(2, 4))

    def get_links_to_papers(self) -> None:
        """
        create paper link list

        Returns
        -------

        """
        if self.check_for_multiple_pages():
            for i in range(self.page_count):
                self.offset = f"&offset={100 * i}"
                self.init_driver()
                self.post_request(self.construct_full_link())
                self.mine_links()

                print(f'reading page: {i + 1} from {self.page_count}', end='\r')

                self.close_driver()

        else:
            self.init_driver()
            self.post_request(self.construct_full_link())
            self.mine_links()
            self.close_driver()

    def to_json(self, path: str) -> None:
        """
        dump results into json

        Parameters
        ----------
        path: str
            string path for save results (link and additional details)

        Returns
        -------

        """
        with open(path, 'w') as file:
            json.dump(self.links_to_paper, file)
