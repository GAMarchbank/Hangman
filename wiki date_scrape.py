import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
import datetime 
import random
from win11toast import toast
import os


# this program uses the datetime modual, the requests modual and the BeautifulSoup modual to scrape a list of people who died on that day. It then selects one at random
# and using the win11toast modual creates a windows notificaion that displays the deceaseds year of death, name and a short biography.

# the entire program is contianed within a while loop, allowing the program to restart if it encounters any issues.
while True:
    # the program begins by calling up a datetime object and then transforming the object into a string that mirrors the format that appears in wikipedias urls
    month_dic ={'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June', '07': 'July', '08': 'August', '09': 'September', '10':'October', '11': 'November', '12': 'December'}
    time = str(datetime.datetime.now().date())
    time = time.split('-')
    search_string = f"{month_dic[time[1]]}_{time[2]}"
    dead_people_lst = []
    # using this configured string the code performs a get request and then extrats the webpage source code using BeautifulSoup
    soup = BeautifulSoup(requests.get(f'https://en.wikipedia.org/wiki/{search_string}').text, 'html.parser')
    # this is then searched through for the list of people who died on that particlar day. the data for these people is then added to the dead_people list variable
    d_p = soup.find('span', id='Deaths').findParent()
    while True:
        try:
            d_p = d_p.find_next('h3')
            choice = d_p.find_next('ul')
            choice = choice.find_all('li')
            dead_people_lst += choice
        except Exception:
            break
    # the code then uses the random moduel to randomly select a single indiviual and extracts the url for that indiviuals wikipedia page from the data
    dead_person = random.choice(dead_people_lst)
    dead_person = dead_person.find_all('a')
    for items in dead_person:
        href = items.get('href')
        check = href.split('/')
        try:
            int(check[2])
        except Exception:
            break
    # this whole next section is contatined within a try. while most wikipedia pages follow similar scripting, there are some differences. 
    # by encasing this in a try. If these differences would crash the program the program simply restarts the while loop, and extracts a differnt indiviual. 
    try:
        # the code performs a get request on the individuals url, and extracts an image if it exists, their name, a short description and the year of their death. 
        people_soup = BeautifulSoup(requests.get(f'https://en.wikipedia.org{href}').text, 'html.parser')
        # here the code is searching the code for the image url and saving the image
        try:
            image = people_soup.find('table', class_='infobox')
            image = image.find('a', class_ = 'image').find('img')
            src = f"https:{image['src']}"
            image = Image.open(BytesIO(requests.get(f"https:{image['src']}").content))
            image.save(f"wiki_search/image.{image.format}")
            image_check = True
        except Exception as e:
            image_check = False
        # here is code is extracting the name
        name = people_soup.find('h1', id= 'firstHeading').find('span').text
        # here the code extracts the description
        description = people_soup.find('div', class_ = 'shortdescription').text    
        # here the code extracts the year of the death    
        death_date = people_soup.find('table', class_= 'infobox').find_all('th', class_ = 'infobox-label')
        try:
            day_check = False
            for items in death_date:
                if items.text == 'Died':
                    parent = items.findParent()
            death_date = parent.find('td').text
            death_date = death_date.split(',')
            # here the code removes any additional information from the year of death.
            try:
                month_day = death_date[0].split('(')
                check = month_day[0].split(' ')
                if len(check) == 3 or (len(check) == 4 and check[3] in ['', ' ']):
                    day_check = True
                    month_day = month_day[0]
                else:
                    year = month_day[1].replace(' ', '')
                    month_day = month_day[0]
            except Exception as e:
                month_day = death_date[0]
                year = death_date[1].split('(')
                year = year[0].replace(' ','')
            if day_check == True:
                whole_date = month_day
            else:
                whole_date = month_day + year
            year = whole_date.split(' ')[2]
            # here using the win11toast modual the program creates a windows popup with the relivent information displayed inside. 
            if image_check == True:
                print(image_check)
                toast(f"{name}\t{year}", description, icon = src)
                print(src)
            else:
                print(image_check)
                toast(f"{name}\t{year}", description)
        except Exception:
            continue
        break
    except Exception:
        continue

