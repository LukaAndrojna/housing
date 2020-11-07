import config
import page_parser
import local_config

import requests
import threading
import concurrent.futures
from bs4 import BeautifulSoup


class Listings:
    def __init__(self):
        self._successful_listings = [','.join(config.feature_names)]
        self._failed_listings = list()
        self._lock = threading.Lock()
    
    def parse_listing(self, ad):
        features, success = page_parser.get_listing_entry(ad)
        with self._lock:
            if success:
                self._successful_listings.append(features)
            else:
                self._failed_listings.append(features)
    
    def successful_output(self) -> str:
        return '\n'.join(self._successful_listings)
    
    def failed_output(self) -> str:
        return '\n'.join(self._failed_listings)


def main():
    listings = Listings()

    for sub in config.SUB_GROUPS:
        for i in range(1,1000):

            page = requests.get(config.DEFAULT_URL + sub + f'{i}/')
            soup = BeautifulSoup(page.content, 'html.parser')

            ads = soup.find_all('div', attrs={'class':'oglas_container', 'itemtype': 'http://schema.org/ListItem'})
            ads_len = len(ads)
            if ads_len == 0:
                break
            with concurrent.futures.ThreadPoolExecutor(max_workers=ads_len) as executor:
                for ad in ads:
                    executor.submit(listings.parse_listing, ad)

    with open(local_config.csv_file, 'w', encoding='utf-8') as f:
        f.write(listings.successful_output())

    with open(local_config.txt_file, 'w', encoding='utf-8') as f:
        f.write(listings.failed_output())

if __name__ == "__main__":
    main()