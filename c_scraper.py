import requests as rq
import bs4 as bs
import traceback
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import glob, os, time
import csv
from csv import writer

# # run the bellow file, if it gives an erro, it means you need to install chrome driver and put it in your path
# # this opens a chrome "site" based on the link below which we will scrape from
driver = webdriver.Chrome(executable_path="/home/cate/Downloads/chromedriver_linux64/chromedriver")
driver.get("https://www.property24.com/for-sale/cape-town/western-cape/432?PropertyCategory=House%2cApartmentOrFlat%2cTownhouse")
page_soup = bs.BeautifulSoup(driver.page_source,'lxml')

dict_data = {"location" :[], "price":[], "floor_size":[], "bathrooms":[], "bedrooms":[],"parking":[] }
icons = page_soup.find_all("span", class_= "p24_icons")
info = page_soup.find_all("div", class_= "p24_regularTile js_rollover_container")

def getValues(icons, info):
    
    for values in info:
        price = values.find('span', class_= 'p24_price')
        if price:
            price = price.text
        else:
            ""
        location = values.find('span', class_= "p24_location")
        if location:
            location = location.text 
        else:
            ""
        
        dict_data["price"].append(price)
        dict_data["location"].append(location)
        #print(price)

    for value in icons:
        floor_size = value.find("span", class_= "p24_size")
        if floor_size:
            floor_size = floor_size.find("span").text
        else:
            ""
        bathrooms = value.find("span", {"title": "Bathrooms"})
        if bathrooms:
            bathrooms = bathrooms.find("span").text
        else:
            ""
        bedrooms = value.find("span", {"title": "Bedrooms"})
        if bedrooms:
            bedrooms = bedrooms.find("span").text
        else:
            ""
        parking = value.find("span", {"title": "Parking Spaces"})
        if parking:
            parking = parking.find("span").text
        else: 
            ""
        dict_data["floor_size"].append(floor_size)
        dict_data["bathrooms"].append(bathrooms)
        dict_data["bedrooms"].append(bedrooms)
        dict_data["parking"].append(parking)
    return dict_data

def append_list_as_row(file_name, dict_data, field_names):
# Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        writer = csv.DictWriter(write_obj, fieldnames = field_names)
        writer.writerow(dict_data)
    
csv_file = "final.csv"
count = 0
while True:
    try:
        driver.implicitly_wait(10)
        page_soup = bs.BeautifulSoup(driver.page_source,'lxml')
        icons = page_soup.find_all("span", class_= "p24_icons")
        info = page_soup.find_all("div", class_= "p24_regularTile js_rollover_container")
        dict_data = {"location" :[], "price":[], "floor_size":[], "bathrooms":[], "bedrooms":[],"parking":[] }
        dict_data = getValues(icons, info)
        field_names = dict_data.keys()
        append_list_as_row('final.csv', dict_data, field_names)
        count+= 1
        print(f'{count}\r', end = "")
        loadmore = driver.find_element_by_link_text("Next").click()
        time.sleep(5)
        #loadmore.send_keys(Keys.ENTER)
        
    except Exception:
        print("Reached bottom of page")
        traceback.print_exc()
        break