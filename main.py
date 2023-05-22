import os

from datetime import datetime
from src.scidirect import ScienceDirect, Paper as SDP
from src.acm import ACM, Paper as ACMP
from src.ieee import IEEE, Paper as IXP
from src.utils import *

if __name__ == "__main__":
    config = read_json("./config.json")
    assert validate(config)

    if not os.path.isdir('temp'):
        os.mkdir('temp')

    if not os.path.isdir('abs'):
        os.mkdir('abs')

    scrappers = {'IEEE', 'ACM', 'SCIDIR'}.intersection(set(config.keys()))

    for s in scrappers:
        if s == 'IEEE':
            # get links to individual search results
            ieee = IEEE(config['IEEE']['search_term'])
            ieee.get_links_to_papers()

            # dump links
            if config['IEEE']['keep_link_file']:
                ieee.to_json(config['IEEE']['link_file_save_to'])

            # get abstract of the and every search results
            ieee_paper = IXP(config['IEEE']['link_file_save_to'])

            if config['IEEE']['use_batches']:
                ieee_paper.batch_update_details(config['IEEE']['batch_size'])

            else:
                ieee_paper.update_paper_details()

            if not config['IEEE']['keep_link_file']:
                os.remove(config['IEEE']['link_file_save_to'])

        elif s == 'ACM':
            # get links to individual search results
            current_year = datetime.now().year
            acm = ACM((current_year - 5), current_year, config['ACM']['search_term'])
            acm.get_links_to_papers()

            # dump links
            if config['ACM']['keep_link_file']:
                acm.to_json(config['ACM']['link_file_save_to'])

            # get abstract of the and every search results
            acm_paper = ACMP(config['ACM']['link_file_save_to'])

            if config['ACM']['use_batches']:
                acm_paper.batch_update_details(config['ACM']['batch_size'])

            else:
                acm_paper.update_paper_details()

            if not config['ACM']['keep_link_file']:
                os.remove(config['ACM']['link_file_save_to'])

        elif s == 'SCIDIR':
            # get links to individual search results
            current_year = datetime.now().year
            sd = ScienceDirect((current_year - 5), current_year, config['SCIDIR']['search_term'])
            sd.get_links_to_papers()

            # dump links
            if config['SCIDIR']['keep_link_file']:
                sd.to_json(config['SCIDIR']['link_file_save_to'])

            # get abstract of the and every search results
            sd_paper = SDP(config['SCIDIR']['link_file_save_to'])

            if config['SCIDIR']['use_batches']:
                sd_paper.batch_update_details(config['SCIDIR']['batch_size'])

            else:
                sd_paper.update_paper_details()

            if not config['SCIDIR']['keep_link_file']:
                os.remove(config['SCIDIR']['link_file_save_to'])

        else:
            raise ConfigurationError(f"wrong scrapper {s}.")
