# -*- coding: utf-8 -*-
"""autoscout24-scrape.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xwgBCdRvgsgP4AOmbafHE8ervHtRDhh_

!pip install bs4
!pip install requests
!pip install pandas
!pip install numpy
"""

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

HEADERS = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

# list to store url of all cars on autoscout24.be
all_url = []

# send request to the 20 accessible pages on the website and scrape the url of each car
# store in list -> "all_url"

for each_page in range(1, 21):
  webpage = requests.get(f"https://www.autoscout24.be/nl/lst?sort=standard&desc=0&ustate=N%2CU&atype=C&cy=B&search_id=10hyyuturim&page={each_page}", headers=HEADERS)
  # webpage.content
  soup = BeautifulSoup(webpage.content, "html.parser")
  links = soup.find_all("a", attrs={'class': 'ListItem_title__znV2I Link_link__pjU1l'})
  for i in range(0, 20):
    all_url.append(links[i].get("href"))

# all_url now contains links to all the cars on the website
len(all_url)

# Functions to scrape each property

# scrape name
def get_name(soup):
  try:
    name = soup.find('span', attrs={'class':'StageTitle_boldClassifiedInfo__L7JmO'}).text
  except AttributeError:
    name = ""

  return name

# scrape model
def get_model(soup):
  try:
    model = soup.find('span', attrs={'class':'StageTitle_model__pG_6i StageTitle_boldClassifiedInfo__L7JmO'}).text
  except AttributeError:
    model = ""

  return model

# scrape price
def get_price(soup):
  try:
    price = soup.find('span', attrs={'class':'StandardPrice_price__X_zzU'}).text.split(",")[0]
  except AttributeError:
    price = ""

  return price

# scrape kilometers
def get_kilometers(soup):
  try:
    kilometers = soup.find_all('div', attrs={'class':'VehicleOverview_itemContainer__Ol37r'})[0].find('div', attrs={'class':'VehicleOverview_itemText__V1yKT'}).text
  except AttributeError:
    kilometers = ""

  return kilometers

# scrape transmission
def get_transmission(soup):
  try:
    transmission = soup.find_all('div', attrs={'class':'VehicleOverview_itemContainer__Ol37r'})[1].find('div', attrs={'class':'VehicleOverview_itemText__V1yKT'}).text
  except AttributeError:
    transmission = ""

  return transmission

# scrape manufactured_date
def get_manufactured_date(soup):
  try:
    manufactured_date = soup.find_all('div', attrs={'class':'VehicleOverview_itemContainer__Ol37r'})[2].find('div', attrs={'class':'VehicleOverview_itemText__V1yKT'}).text
  except AttributeError:
    manufactured_date = ""

  return manufactured_date

# scrape fuel_type
def get_fuel_type(soup):
  try:
    fuel_type = soup.find_all('div', attrs={'class':'VehicleOverview_itemContainer__Ol37r'})[3].find('div', attrs={'class':'VehicleOverview_itemText__V1yKT'}).text
  except AttributeError:
    fuel_type = ""

  return fuel_type

# scrape power
def get_power(soup):
  try:
    power = soup.find_all('div', attrs={'class':'VehicleOverview_itemContainer__Ol37r'})[4].find('div', attrs={'class':'VehicleOverview_itemText__V1yKT'}).text
  except AttributeError:
    power = ""

  return power

# scrape model
def get_seller(soup):
  try:
    seller = soup.find_all('div', attrs={'class':'VehicleOverview_itemContainer__Ol37r'})[5].find('div', attrs={'class':'VehicleOverview_itemText__V1yKT'}).text
  except AttributeError:
    seller = ""
    
  return seller

# dict to values in each col
first_data = {
    "name": [],
    "model": [],
    "price": [],
    "kilometers": [],
    "transmission": [],
    "manufactured_date": [],
    "fuel_type": [],
    "power": [],
    "seller": []
}

# scrape data from each url
for url in all_url:
  webpage = requests.get(f"https://www.autoscout24.be{url}", headers=HEADERS)
  soup = BeautifulSoup(webpage.content, "html.parser")

  first_data['name'].append(get_name(soup))

  first_data['model'].append(get_model(soup))

  first_data['price'].append(get_price(soup))

  first_data['kilometers'].append(get_kilometers(soup))

  first_data['transmission'].append(get_transmission(soup))

  first_data['manufactured_date'].append(get_manufactured_date(soup))

  first_data['fuel_type'].append(get_fuel_type(soup))

  first_data['power'].append(get_power(soup))

  first_data['seller'].append(get_seller(soup))

len(first_data['fuel_type'])

# creatre a dataframe using the 'first_data' dict
autoscout24_df = pd.DataFrame.from_dict(first_data)

autoscout24_df['kilometers'].replace('-', '', inplace=True)
autoscout24_df['manufactured_date'].replace('-', '', inplace=True)
autoscout24_df['fuel_type'].replace('-', '', inplace=True)

autoscout24_df.head(15)

"""
Data Explanation

name - name of car
model - car model
price - car price in Euros
kilometers - amount of kilometers already on the car in KM
transmission - manual or automatic
manufactured_date - year car was manufactured
fuel_type - type of fuel the car uses
power - car power in KW and horsepower(in bracket)
seller - car seller

"""

# save df to csv file
autoscout24_df.to_csv('autoscout24-cars.csv')



# trying to scrape more data ...
grab_basic_data_title = soup.find_all('div', attrs={'class':'DetailsSection_childrenSection__NQLD7'})[2].find_all('dt', attrs={'class':'DataGrid_defaultDtStyle__yzRR_'})
basic_data_title = [j.text for j in grab_basic_data_title]
print(basic_data_title)

grab_basic_data_value = soup.find_all('div', attrs={'class':'DetailsSection_childrenSection__NQLD7'})[2].find_all('dd', attrs={'class':'DataGrid_defaultDdStyle__29SKf DataGrid_fontBold__r__dO'})
basic_data_value = [j.text for j in grab_basic_data_value]
print(basic_data_value)

# take length of each list, know how I can iterate through both
# have a dictionary containing all possible properties and then assign values to the ones that have

# iterate through dict and see if title/key in list, get the index and use the index to select its value in the value list and add the value in the value list in dict

