import config
import local_config
from listings import Listings

import requests
import concurrent.futures
from bs4 import BeautifulSoup


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