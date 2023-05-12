from models.scidirect import ScienceDirect
from models.acm import ACM


def get_links_to_acm_publications(query_text, file_name):
    search = ACM(start=2018, end=2023, search_terms=query_text)
    search.get_links_to_papers()
    search.to_json(f'./data/{file_name}')


def get_links_to_sci_direct_publications(query_text, file_name):
    search = ScienceDirect(start=2015, end=2023, search_terms=query_text)
    search.get_links_to_papers()
    search.to_json(f'./data/{file_name}')


if __name__ == "__main__":
    acm_query = "Keyword:(image segmentation OR semantic segmentation) AND AllField:(u-net) AND AllField:(forests) AND " \
                "AllField:(\"remote sensing\" OR \"satellite images\")"
    sci_direct_query = "semantic segmentation;u-net;forests;remote sensing;"

    acm_dump = "acm_search_term_1.json"
    sci_direct_dump = "scidir_search_term_1.json"

    # get_links_to_acm_publications(acm_query, acm_dump)
    get_links_to_sci_direct_publications(sci_direct_query, sci_direct_dump)
