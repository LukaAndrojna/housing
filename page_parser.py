import config
import extractors

import requests
from typing import Tuple
from bs4 import BeautifulSoup, element


def parse_info(info: str):
    a = list()
    for item in info.split(' | '):
        item = item.split(': ')
        if len(item) == 2:
            a.append(item[1])
        else:
            a.append(None)
    return tuple(a)
    

def get_page_data(URL: str):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    info = soup.find_all('div', class_='more_info')[0]
    summary = soup.find_all('div', class_='kratek')[0]
    if info != None:
        info = info.text.strip()
        summary = summary.text.strip()
        return (info, summary)
    
    return ('','')

def get_listing_entry(ad: element.Tag) -> Tuple[str, bool]:
    href = ad.find_all('a', href=True)[0]['href']
    URL = config.DEFAULT_URL + href

    info, summary = get_page_data(URL)
    summary = summary.split('Rok oddaje')[0]
    summary = summary.split('Datum dražbe')[0]
    #print(summary)
    try:
        offer_type, propety_type, region, subregion, commune = parse_info(info)
        propety_type = config.propety_types[propety_type]
        location = extractors.extract_location(summary)
        floor_area = extractors.extract_area(summary)
        property_type = extractors.extract_type(summary)
        built = extractors.extract_year_built(summary)
        adapted = extractors.extract_year_adapted(summary)
        land = extractors.extract_land(summary)
        price, m2_price = extractors.extract_price(summary, floor_area)
        floor = extractors.extract_floor(ad)
        features = [
            location,
            floor_area,
            property_type,
            built,
            adapted,
            land,
            floor,
            price,
            m2_price,
            offer_type,
            propety_type,
            region,
            subregion,
            commune]

        return (','.join([str(ftr).replace(',', ' /') if type(ftr) != float else f'{ftr:.2f}' for ftr in features]), True)
    except:
        return (summary, False)