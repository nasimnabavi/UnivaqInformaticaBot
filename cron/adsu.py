#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This script scrapes all the info about the adsu of the university's city."""

import sys
sys.path.insert(0, '../')
import requests

from bs4 import BeautifulSoup
from libs.utils import utils

def scrape_adsu():
    """Get information about the adsu in a crazy way due to their bitching page made like shit"""

    scraped_info = {}
    adsu_url = "http://www.adsuaq.org/"
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5)",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
        "accept-encoding": "gzip,deflate,sdch",
        "accept-language": "en-US,en;q=0.8",
    }

    request = requests.get(adsu_url, headers=headers)

    if request.status_code != 200:
        print("Error! Status "+request.status_code)
        return

    info = BeautifulSoup(request.text, "html.parser").find(id="AutoNumber5").text.replace("  ", "")\
           .replace("\t", "").replace("\r", "").replace("\n\n", "")

    scraped_info.update({
        "info": info
    })

    utils.write_json(scraped_info, "../json/adsu.json")

if __name__ == "__main__":
    scrape_adsu()
