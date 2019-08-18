# -*- coding: utf-8 -*-
"""
This code outputs two .json files:
    - br_states.json: contains states in Brazil
    - br_cities.json: contains cities in Brazil

By Verona Montone
"""

import json
import requests

from bs4 import BeautifulSoup


def save_json(file_name, data):
    with open('{}.json'.format(file_name), 'w') as f:
        json.dump(data, f)


def main():
    # Get states in Brazil, which are hard coded in Canal Rural web page
    # Read web page
    canalrural_url = 'https://tempo.canalrural.uol.com.br/previsao/10-dias'
    r = requests.get(canalrural_url)
    html_doc = r.text

    soup = BeautifulSoup(html_doc, 'html.parser')
    print(soup.prettify())

    # Extract states from html
    states_options = soup.find(id="lista-estados").findChildren('option')

    states = dict()
    for option in states_options:
        states[option.get('value')] = option.get_text()

    # Get cities in Brazil
    cities = dict()
    for s in states.keys():
        print('Getting cities for {}'.format(s))
        try:
            url4get = "https://tempo.canalrural.uol.com.br/ajax/10-dias/{}".format(s)
            r = requests.get(url=url4get)
            cities[s] = r.json()
        except:
            'error in request for state {}'.format(s)

    # Save
    save_json('br_states', states)
    save_json('br_cities', states)


if __name__ == '__main__':
    main()