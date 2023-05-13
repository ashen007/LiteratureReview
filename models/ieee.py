import time
import requests
import numpy as np
import json
import undetected_chromedriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth


class IEEE:
    """
    Parameters
    ----------
    query: str
        search term for either simple search or advanced search, if for advanced
        search need to add AND, OR, NOT in between search keywords.

    Attributes
    ----------
    headers: dict
        header to post for IEEE Xplore

    payload: dict
        additional details for filter results from request

    page_count: int
        total number of pages in the search results

    links_to_paper: dict
        mined links and additional details for results

    Methods
    -------
    post_request:
        send request to IEEE server

    check_for_multiple_pages:
        check weather results has been divide to multiple
        web pages, if so update the page count.

    mine_links:
        get links for each document from search results

    get_links_to_papers:
        add all links to single object

    to_json:
        dump links to json file

    """

    def __init__(self, query):
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://ieeexplore.ieee.org",
            "Content-Type": "application/json",
        }
        self.payload = {
            "newsearch": True,
            "queryText": query,
            "highlight": True,
            "returnFacets": ["ALL"],
            "returnType": "SEARCH",
            "pageNumber": 1
        }
        self.page_count = None
        self.links_to_paper = {}

    @staticmethod
    def post_request(header: dict, json: dict) -> requests.Response:
        """
        send request to IEEE server

        Parameters
        ----------
        header: dict
            header to post for IEEE Xplore

        json: dict
            additional details for filter results from request

        Returns
        -------

        """
        result = requests.post("https://ieeexplore.ieee.org/rest/search",
                               headers=header,
                               json=json)

        return result

    def check_for_multiple_pages(self) -> bool:
        """
        check weather results has been divide to multiple
        web pages, if so update the page count.

        Returns
        -------

        """
        results = self.post_request(self.headers, self.payload).json()
        self.page_count = results['totalPages']

        return True if self.page_count > 1 else False

    def mine_links(self) -> None:
        """
        get links for each document from search results

        Returns
        -------

        """
        request = self.post_request(self.headers, self.payload)
        j = 1

        while request.status_code != 200:
            time.sleep(abs(np.random.normal(0.1, 2)))
            request = self.post_request(self.headers, self.payload)

        results = request.json()

        for record in results['records']:
            self.links_to_paper[record['articleNumber']] = [record.get('articleTitle', None),
                                                            record.get('documentLink', None),
                                                            record.get('publicationYear', None)]

    def get_links_to_papers(self) -> None:
        """
        add all links to single object

        Returns
        -------

        """
        if self.check_for_multiple_pages():
            for i in range(1, (self.page_count + 1)):
                self.payload["pageNumber"] = i

                self.mine_links()

                print(f'reading page: {i} from {self.page_count}', end='\r')

        else:
            self.mine_links()

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


class Paper:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.binary_location = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'

    def __init__(self, file_name):
        self.driver = None
        self.destination = file_name

        with open(file_name, "r") as file:
            self.link_object = json.load(file)

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

    def request_paper(self, page_link) -> None:
        """
        post a request to science direct server

        Parameters
        ----------
        page_link: str
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

        URL = f"https://ieeexplore.ieee.org{page_link}"

        # make request
        self.driver.delete_all_cookies()
        self.driver.get(URL)

        time.sleep(abs(np.random.normal(1, 0.4)))

    def get_abstract_text(self) -> str:
        """
        get abstract from each publication

        Returns
        -------
        abstract: str

        """
        return self.driver.find_element(By.CLASS_NAME, 'abstract-text').text.replace('Abstract:\n', '')

    def click_kw_section(self) -> None:
        self.driver.execute_script("arguments[0].scrollIntoView();",
                                   self.driver.find_element(By.ID, 'keywords'))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'keywords'))).click()
        time.sleep(1)

    def get_keywords(self) -> list:
        """
        get all type of keywords in ieee xplore for the publication

        Returns
        -------
        list of keyword strings: list

        """
        kw_types = self.driver.find_elements(By.CSS_SELECTOR,
                                             "ul[class='doc-keywords-list stats-keywords-list']>li["
                                             "class='doc-keywords-list-item']>ul")
        return [kw.text.replace('\n', '') for kw in kw_types if kw.text != '']

    def update_paper_details(self) -> None:
        """
        update the detail object of the publications

        Returns
        -------

        """
        # start driver
        self.init_driver()

        for key, value in self.link_object.items():
            doc_link = value[1]
            self.request_paper(doc_link)
            self.click_kw_section()

            time.sleep(abs(np.random.normal(1, 0.4)))

            try:
                abstract = self.get_abstract_text()
                kws = self.get_keywords()

            except:
                abstract = np.NAN
                kws = np.NAN

            if abstract not in value:
                value.append(abstract)

            if kws not in value:
                value.append(kws)

        # close driver
        self.close_driver()

    def batch_update_details(self, size) -> None:
        """
        update the detail object of the publications batch wise

        Parameters
        ----------
        size: int
            size of a batch

        Returns
        -------

        """
        keys = list(self.link_object.keys())

        for i in range(size, len(self.link_object), size):
            batch = keys[(i - size):i]
            self.init_driver()

            for p in batch:
                doc_link = self.link_object[p][1]
                self.request_paper(doc_link)
                self.click_kw_section()

                try:
                    abstract = self.get_abstract_text()
                    kws = self.get_keywords()

                except:
                    abstract = np.NAN
                    kws = np.NAN

                if abstract not in self.link_object[p]:
                    self.link_object[p].append(abstract)

                if kws not in self.link_object[p]:
                    self.link_object[p].append(kws)

            # dump updated link object to json
            self.to_json('./data/temp.json')

            # close driver
            self.close_driver()

    def to_json(self, path) -> None:
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
            json.dump(self.link_object, file)
