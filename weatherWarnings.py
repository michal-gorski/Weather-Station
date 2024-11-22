import requests
import urllib3
import json
from PIL import Image,ImageDraw,ImageFont
import imageHelper

class WeatherWarnings:
    weatherWarning = []
    def __init__(self) -> None:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get('https://danepubliczne.imgw.pl/api/data/warningsmeteo',verify=False)
        parsed = response.json()
        if parsed['status'] != False:
            filteredEvent = [event for event in parsed if "2261" in event['teryt']]
            
            for event in filteredEvent:            
                self.weatherWarning.append(event['tresc'])   
        
    def PrintWarnings(self):   
        for warning in self.weatherWarning:
            print(warning)
            print('//////////')

    def DrawWarnings(self,draw:ImageDraw.ImageDraw,fonts,x1:int,y1:int,x2:int,y2:int):
        if len(self.weatherWarning) == 0:
            draw.text((x1+5,y1+8),"• Brak ostrzeżeń",0,fonts['font14light'])
        elif len(self.weatherWarning) == 1:
            wrappedText = imageHelper.WrappedText('• '+self.weatherWarning[0],fonts['font14light'],x2-x1-10)
            draw.text((x1+5,y1+8),wrappedText,0,fonts['font14light'])
        elif len(self.weatherWarning) >= 1:
            for warning in self.weatherWarning:
                wrappedText = imageHelper.WrappedText('• '+warning,fonts['font10light'],x2-x1-10)
                draw.text((x1+5,y1+8),wrappedText,0,fonts['font10light'])