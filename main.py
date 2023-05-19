from src.scidirect import ScienceDirect, Paper
from src.acm import ACM, Paper
from src.ieee import IEEE, Paper
from src.utils import read_json


def get_links_to_acm_publications(query_text, file_name):
    search = ACM(start=2018, end=2023, search_terms=query_text)
    search.get_links_to_papers()
    search.to_json(f'./data/{file_name}')


def get_links_to_sci_direct_publications(query_text, file_name):
    search = ScienceDirect(start=2015, end=2023, search_terms=query_text)
    search.get_links_to_papers()
    search.to_json(f'./data/{file_name}')


if __name__ == "__main__":
    config = read_json("./config.json")

