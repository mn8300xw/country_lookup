import requests
from typing import NamedTuple, List, Optional


class CountryInfo(NamedTuple):
    official_name: Optional[str]
    common_name: Optional[str]
    capital: Optional[str]
    region: Optional[str]
    subregion: Optional[str]
    population: Optional[int]
    area: Optional[float]
    cca2: Optional[str]
    cca3: Optional[str]
    flag_png: Optional[str]
    flag_svg: Optional[str]
    currencies: List[str]
    languages: List[str]


def get_country_name(country_code):
    """Return (found, data, error).

    - If found: (True, data_dict, None)
    - If not found: (False, None, None)
    - On error: (False, None, error_message)

    `data_dict` contains keys: `official_name`, `common_name`, `capital`, `region`,
    `subregion`, `population`, `area`, `cca2`, `cca3`, `flag_png`, `flag_svg`,
    `currencies` (list), `languages` (list).
    """

    try:
        url = create_url(country_code)
        json_response = make_api_request(url)
        if not json_response:
            return False, None, None
        data = get_country_info_from_response(json_response)
        return True, data, None
    except Exception:
        return False, None, 'Error connecting to API'

def create_url(country_code):
    url = f'https://restcountries.com/v3.1/alpha/{country_code}'
    return url


def make_api_request(url):
    response = requests.get(url)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    json = response.json()  
    return json


def get_country_info_from_response(json_response) -> CountryInfo:
    obj = json_response[0]
    name_info = obj.get('name', {})
    official_name = name_info.get('official')
    common_name = name_info.get('common')

    # capital
    capital = None
    capital_list = obj.get('capital')
    if capital_list and isinstance(capital_list, list) and len(capital_list) > 0:
        capital = capital_list[0]

    # region/subregion
    region = obj.get('region')
    subregion = obj.get('subregion')

    # population/area
    population = obj.get('population')
    area = obj.get('area')

    # codes
    cca2 = obj.get('cca2')
    cca3 = obj.get('cca3')

    # flags
    flags = obj.get('flags') or {}
    flag_png = None
    flag_svg = None
    if isinstance(flags, dict):
        flag_png = flags.get('png')
        flag_svg = flags.get('svg')

    # currencies -> list of strings like 'Euro (€)'
    currencies = []
    curr_obj = obj.get('currencies')
    if isinstance(curr_obj, dict):
        for code, info in curr_obj.items():
            if isinstance(info, dict):
                name = info.get('name')
                symbol = info.get('symbol')
                if name and symbol:
                    currencies.append(f"{name} ({symbol})")
                elif name:
                    currencies.append(name)
                else:
                    currencies.append(code)

    # languages -> list
    languages = []
    lang_obj = obj.get('languages')
    if isinstance(lang_obj, dict):
        languages = list(lang_obj.values())

    return CountryInfo(
        official_name=official_name,
        common_name=common_name,
        capital=capital,
        region=region,
        subregion=subregion,
        population=population,
        area=area,
        cca2=cca2,
        cca3=cca3,
        flag_png=flag_png,
        flag_svg=flag_svg,
        currencies=currencies,
        languages=languages,
    )


def get_capital_from_response(json_response):
    # The API returns a list of capitals under the 'capital' key (may be missing)
    capital_list = json_response[0].get('capital')
    if capital_list and isinstance(capital_list, list) and len(capital_list) > 0:
        return capital_list[0]
    return None
