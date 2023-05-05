import time
import requests
import numpy as np
import json


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
            time.sleep(np.random.normal(0.1, 2))
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
