"""
This script retrieves weather forecast data from Canal Rural web page, powered
by Somar Meteorologia.

By Verona Montone
"""

import re
import datetime
import requests

from bs4 import BeautifulSoup


def get_temperatures(soup):
    temperatures_span = soup.find_all('span', {'class': 'valor-temp-card-verde'})
    temperatures = []
    for t in temperatures_span:
        temp_celcius = t.get_text()
        temp_value = temp_celcius.replace(u'\xba', '')
        temperatures.append(int(temp_value))
    temperatures.sort()
    return {'temp_min_celsius': temperatures[0],
            'temp_max_celsius': temperatures[1]}

def get_precipitation(wx_summary_soup):
    span_values = wx_summary_soup.find_all('span',
                                           {'class': 'valor-card-verde'})
    for span in span_values:
        value = span.get_text()
        if re.findall(r'[0-9]+mm|[0-9]+%', value):
            if re.findall(r'[0-9]+mm', value):
                extract_precip_mm = re.findall(r'[0-9]+mm', value)[0]
                precip_mm = int(extract_precip_mm.replace('mm', ''))
            if re.findall(r'[0-9]+%', value):
                extract_precip_pct = re.findall(r'[0-9]+%', value)[0]
                precip_pct = int(extract_precip_pct.replace('%', ''))
    return {'precip_mm': precip_mm, 'precip_pct': precip_pct}

def get_wx(state, city, wx_day):
    '''
    Returns a dict containing temperature and precipitation weather forecast
    (wx) for a given day from Somar.
    Args:
    state: string for state, e.g. 'sp'
    city: string for city, e.g. 'piracicaba-sp'
    wx_day: int for wx day, e.g. today's wx equals 0, tomorrow's equals 1 
    '''
    try:
        wx_date = (datetime.datetime.now() + datetime.timedelta(wx_day)).strftime('%Y-%m-%d')
        base_url = "https://tempo.canalrural.uol.com.br/previsao/10-dias"
        url4get = "{url}/{state}/{city}/{date}".format(url=base_url,
                                                       state=state,
                                                       city=city,
                                                       date=wx_date)
        r = requests.get(url4get)
        html_doc = r.text
        soup = BeautifulSoup(html_doc, 'html.parser')
        wx_summary = soup.find('section', {'class': 'card-verde'})
        wx = {'wx_date': wx_date}
        wx.update(get_temperatures(wx_summary))
        wx.update(get_precipitation(wx_summary))
        return wx
    except:
        return {}

def get_somar_wx(state, city):
    # Get wx for the next 7 days + today
    wx_range_in_days = 7
    somar_7day_wx = {}

    for day in range(0, wx_range_in_days+1):
        somar_7day_wx['wx_day_{}'.format(day)] = get_somar_wx(state, city, day)
    return somar_7day_wx
