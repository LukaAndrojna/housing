import re
from typing import Tuple, List


def remove_substrings(s: str, arr: List) -> str:
    for ss in arr:
        s = s.replace(ss, '')
    return s

def parse_str_to_float(s: str) -> float:
    s = s.replace('.', '').replace(',', '.')
    return float(s)

def extract_area(s: str) -> float:
    area = re.findall(r'[0-9,\.]+ m2', s)
    if len(area) == 0:
        return None
    area = area[0]
    return parse_str_to_float(area.replace(' m2', ''))

def extract_price(s: str, area: float) -> Tuple[float, float]:
    price = ''
    if 'EUR' not in s:
        return (None, None)
    for opt in ['Cena: ', 'Izhodiščna cena: ', 'Izklicna cena: ']:
        if opt in s:
            price = s.split(opt)[-1]
    price = remove_substrings(price, ['do ', 'min. ', 'max. ', 'cca ', ''])
    
    if s.endswith('EUR/m2') or s.endswith('EUR/m2/mes'):
        price = remove_substrings(price, [' EUR/m2', '/l', '/mes', '/ted', '/dan'])
        price = parse_str_to_float(price)
        return price * area, price
    price = remove_substrings(price, [' EUR', '/l', '/mes', '/ted', '/dan'])
    price = parse_str_to_float(price)
    area_price = None
    if area > 0:
        area_price = price / area
    return price, area_price

def extract_location(s: str) -> str:
    return s.split(',')[0].lower()

def extract_type(s: str) -> str:
    return s.split('m2,')[1].split(',')[0].lower()

def extract_year_built(s: str) -> int:
    built = re.findall(r'zgrajeno l. [0-9]{4},', s)
    if len(built) == 0:
        return None
    built = built[0]
    if ' ' in built:
        return int(remove_substrings(built, ['zgrajeno l. ', ',', '']))
    return None

def extract_year_adapted(s: str) -> int:
    adapted = re.findall(r'adaptirano  l. [0-9]{4},', s)
    if len(adapted) == 0:
        return None
    adapted = adapted[0]
    return int(remove_substrings(adapted, ['adaptirano l. ', ',']))

def extract_land(s: str) -> float:
    land = re.findall(r', [0-9]+ m2 zemljišča,', s)
    if len(land) == 0:
        return None
    land = land[0]
    return parse_str_to_float(remove_substrings(land, [', ', ' m2 zemljišča,'])) 

def extract_floor(s: str) -> int:
    floor_mapping = {
        '2K': -2,
        'K': -1,
        'PK': -0.5,
        'P': 0,
        'VP': 0,
        'M': 0.5,
        'ME': 0.5
    }

    s = s.find_all('div', attrs={'class':'atributi'})
    if len(s) == 0:
        return None
    s = s[0].text.strip()
    s = re.findall(r'Nadstropje: .+/', s)
    if len(s) == 0:
        return None

    floor = remove_substrings(s[0], ['/', 'Nadstropje: '])
    if floor in floor_mapping:
        return floor_mapping[floor]
    return floor
