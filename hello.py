import random
import requests
from bs4 import BeautifulSoup

#print("Hello World")

numbers = {}

count = 100
sum =0
for x in range(count):
    rand = random.randint(1,6)
    sum += rand
    numbers.setdefault(rand,0)
    numbers[rand] += 1


#print(sum/count)
#print("------------------")
#print(dict(sorted(numbers.items())))


url = 'https://weather.com/pl-PL/weather/tenday/l/93409ef628e2eccc8fe84493beb24470c722d12ef4632a9c49250af345ba81ef'

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

response = requests.get(url,verify=False)

soup = BeautifulSoup(response.text, 'html.parser')
mydivs = soup.find_all("div")

filteredDivs = []
for div in mydivs:
    testId = div.get('data-testid')
    if testId=='DailyContent': 
        filteredDivs.append(div)

forecast = {}

for div in filteredDivs:  
    day = div.h2.text 
    forecast[day] = dict() 
    
    forecast[day]['temperature'] = div.find_all(attrs={"data-testid": "TemperatureValue"})[0].text
    forecast[day]['wind'] = div.find_all(attrs={"data-testid": "Wind"})[0].text.replace(u'\xa0', u' ')
    forecast[day]['rain'] = div.find_all(attrs={"data-testid": "PercentageValue"})[0].text.replace(u'\xa0', u' ')
    forecast[day]['icon'] = div.find_all(attrs={"data-testid": "weatherIcon"})[0].text

#f = open("divs.txt", "a")
#f.write(copiedDivs)
#f.close()

for forecastDay in forecast:
    print(forecastDay,': temperatura: ',forecast[forecastDay]['temperature'], ' | wiatr: ',forecast[forecastDay]['wind'], ' | deszcz: ',forecast[forecastDay]['rain'], ' | opis: ',forecast[forecastDay]['icon'])
    print('-------')


response = requests.get('https://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/736',verify=False)
import json
parsed = response.json()
print('Pył PM 2.5: ',parsed['pm25IndexLevel']['indexLevelName'])
print('Pył PM 10: ',parsed['pm10IndexLevel']['indexLevelName'])

with open('plan.json', 'r') as file:
    data = json.load(file)
    print(data)
