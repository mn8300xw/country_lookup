""" A program for looking up a country's name from a country code. """

import country_api 

def main():
    while True:
        code = input('Enter country code or press enter to quit ')
        # TODO check code is 2 letters 
        # TODO end the loop if user presses enter
        found, data, error = country_api.get_country_name(code)

        if found:
            # `data` is a CountryInfo NamedTuple
            name = data.official_name or data.common_name
            capital = data.capital
            if capital:
                print(f'{code} is the country code for {name} (capital: {capital})')
            else:
                print(f'{code} is the country code for {name}')
        elif not found and not error:
            print('No country found for that code')
        else:
            print('Error fetching data')
        

main()
