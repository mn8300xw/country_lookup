import requests 

def get_country_name(country_code):
    """ Returns a tuple of found, country name, capital, error
    If country is found, the tuple will be (True, country name, capital, None)
    If country is not found, the tuple will be (False, None, None, None)
    If there is an error connecting to the API, the tuple will be (False, None, None, error message)"""

    try:
        url = create_url(country_code)
        json_response = make_api_request(url)
        if not json_response:
            return False, None, None, None
        name = get_name_from_response(json_response)
        capital = get_capital_from_response(json_response)
        return True, name, capital, None
    except Exception:
        return False, None, None, 'Error connecting to API'

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


def get_name_from_response(json_response):
    name = json_response[0]['name']['official']
    return name


def get_capital_from_response(json_response):
    # The API returns a list of capitals under the 'capital' key (may be missing)
    capital_list = json_response[0].get('capital')
    if capital_list and isinstance(capital_list, list) and len(capital_list) > 0:
        return capital_list[0]
    return None
