import config
import page_parser
import local_config

import requests
from bs4 import BeautifulSoup


failed = []

def main():
    with open(local_config.csv_file, 'w', encoding='utf-8') as f:
        f.write(','.join(config.feature_names))
        for sub in config.SUB_GROUPS:
            for i in range(1,1000):

                page = requests.get(config.DEFAULT_URL + sub + f'{i}/')
                soup = BeautifulSoup(page.content, 'html.parser')

                ads = soup.find_all('div', attrs={'class':'oglas_container', 'itemtype': 'http://schema.org/ListItem'})
                if len(ads) == 0:
                    break
                for ad in ads:
                    features, success = page_parser.get_listing_entry(ad)
                    if success:
                        f.write('\n' + features)
                    else:
                        failed.append(features)

    with open(local_config.txt_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(failed))

if __name__ == "__main__":
    main()
