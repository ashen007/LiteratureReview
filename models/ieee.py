import time
import requests
import numpy as np
import json


class IEEE:

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
    def post_request(header, json):
        result = requests.post("https://ieeexplore.ieee.org/rest/search",
                               headers=header,
                               json=json)

        return result

    def check_for_multiple_pages(self):
        results = self.post_request(self.headers, self.payload).json()
        self.page_count = results['totalPages']

        return True if self.page_count > 1 else False

    def mine_links(self):
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

    def get_links_to_papers(self):
        if self.check_for_multiple_pages():
            for i in range(1, (self.page_count + 1)):
                self.payload["pageNumber"] = i

                self.mine_links()

                print(f'reading page: {i} from {self.page_count}', end='\r')

        else:
            self.mine_links()

    def to_csv(self, path):
        with open(path, 'w') as file:
            json.dump(self.links_to_paper, file)