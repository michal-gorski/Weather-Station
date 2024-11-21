import requests
from bs4 import BeautifulSoup
import urllib3
from PIL import Image,ImageDraw,ImageFont
import imageHelper
import re


class Forecast:
    forecast = {}
    icons={"Mostly Cloudy":1,"Partly Cloudy Night":2,"Scattered Showers Night":3,"Scattered Showers":4,"Partly Cloudy":5,"Sunny":6,"Rain and Snow":7,"Snow":8,"Cloudy":9,"Rain":10,"Mostly Cloudy Night":11,"Scattered Snow Night":12,"Mostly Sunny":13}
    
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
            day = div.h2.text.split('|')[0].strip()
            dayPart = div.h2.text.split('|')[1].strip()
            if day not in self.forecast: self.forecast[day] = dict() 
            self.forecast[day][dayPart] = dict()
            self.forecast[day][dayPart]['temperature'] = div.find_all(attrs={"data-testid": "TemperatureValue"})[0].text
            self.forecast[day][dayPart]['wind'] = div.find_all(attrs={"data-testid": "Wind"})[0].text.replace(u'\xa0', u' ')
            self.forecast[day][dayPart]['rain'] = div.find_all(attrs={"data-testid": "PercentageValue"})[0].text.replace(u'\xa0', u' ')
            self.forecast[day][dayPart]['icon'] = div.find_all(attrs={"data-testid": "weatherIcon"})[0].text

    def PrintForecast(self):
        for forecastDay in self.forecast:
            for dayPart in self.forecast[forecastDay]:
                print(forecastDay,' | ',dayPart,': temperatura: ',self.forecast[forecastDay][dayPart]['temperature'], ' | wiatr: ',self.forecast[forecastDay][dayPart]['wind'], ' | deszcz: ',self.forecast[forecastDay][dayPart]['rain'], ' | opis: ',self.forecast[forecastDay][dayPart]['icon'],':',self.icons[self.forecast[forecastDay][dayPart]['icon']])
                print('-------')

    def DrawForecast(self,draw:ImageDraw.ImageDraw,fonts,x1:int,y1:int,x2:int,y2:int):
        position = 0
        skipFirst = True
        for forecastDay in self.forecast:
            
            if skipFirst != True and position <= 6:
                leftBorder = x1 + round(position * (x2-x1) / 7)
                boxWidth = round((x2-x1) / 7)
                
                #draw box line
                imageHelper.DrawDottedVerticalLine(draw,leftBorder + boxWidth,y1,y2,4)
                
                #draw day title
                dayTextLen = draw.textlength(forecastDay, font=fonts['font14'], direction=None, features=None)
                dayTextPos = round(leftBorder + boxWidth / 2 - dayTextLen / 2)
                draw.text((dayTextPos, y1+5),forecastDay,0,font=fonts['font14'])
                
                #draw weather icon
                draw.rectangle(xy = (leftBorder + 5, y1+25,leftBorder + boxWidth - 5, y1 + 60),fill = 255,outline = 0,width = 1)
                

                #draw temperature
                temperature = self.forecast[forecastDay]['Dzień']["temperature"] + " / " + self.forecast[forecastDay]['Noc']["temperature"]
                tempTextLen = draw.textlength(temperature, font=fonts['font14'], direction=None, features=None)
                tempTextPos = round(leftBorder + boxWidth / 2 - tempTextLen / 2)
                draw.text((tempTextPos, y1+63),temperature,0,font=fonts['font14'])

                #draw wind
                wind = re.findall(r'\d+', self.forecast[forecastDay]['Dzień']["wind"])[0] + ' km/h'
                windTextLen = draw.textlength(wind, font=fonts['font14light'], direction=None, features=None)
                windTextPos = round(leftBorder + boxWidth / 2 - windTextLen / 2)
                draw.text((windTextPos, y1+78),wind,0,font=fonts['font14light'])
                
                position += 1
            
            elif skipFirst == True:
                skipFirst = False
            