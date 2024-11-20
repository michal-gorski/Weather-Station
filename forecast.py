import requests
from bs4 import BeautifulSoup
import urllib3


class Forecast:
    forecast = {}
    icons={"Mostly Cloudy":1,"Partly Cloudy Night":2,"Scattered Showers Night":3,"Scattered Showers":4,"Partly Cloudy":5,"Sunny":6,"Rain and Snow":7,"Snow":8,"Cloudy":9,"Rain":10,"Mostly Cloudy Night":11,"Scattered Snow Night":12}
    
    def __init__(self,url = "https://weather.com/pl-PL/weather/tenday/l/93409ef628e2eccc8fe84493beb24470c722d12ef4632a9c49250af345ba81ef"):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(url,verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        mydivs = soup.find_all("div")

        filteredDivs = []
        for div in mydivs:
            testId = div.get('data-testid')
            if testId=='DailyContent': 
                filteredDivs.append(div)

        for div in filteredDivs:  
            day = div.h2.text 
            self.forecast[day] = dict() 
            self.forecast[day]['temperature'] = div.find_all(attrs={"data-testid": "TemperatureValue"})[0].text
            self.forecast[day]['wind'] = div.find_all(attrs={"data-testid": "Wind"})[0].text.replace(u'\xa0', u' ')
            self.forecast[day]['rain'] = div.find_all(attrs={"data-testid": "PercentageValue"})[0].text.replace(u'\xa0', u' ')
            self.forecast[day]['icon'] = div.find_all(attrs={"data-testid": "weatherIcon"})[0].text

    def PrintForecast(self):
        for forecastDay in self.forecast:
            print(forecastDay,': temperatura: ',self.forecast[forecastDay]['temperature'], ' | wiatr: ',self.forecast[forecastDay]['wind'], ' | deszcz: ',self.forecast[forecastDay]['rain'], ' | opis: ',self.forecast[forecastDay]['icon'],':',self.icons[self.forecast[forecastDay]['icon']])
            print('-------')
