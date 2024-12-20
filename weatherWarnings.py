import requests
import urllib3
import json
from PIL import Image,ImageDraw,ImageFont
import imageHelper
import logging
logger = logging.getLogger(__name__)

class WeatherWarnings: 
    weatherWarning = []
    def __init__(self) -> None:
        logger.info("Getting weather warnings")
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get('https://danepubliczne.imgw.pl/api/data/warningsmeteo',verify=False)
        parsed = response.json()
        if not(hasattr(parsed,'status')) or (hasattr(parsed,'status') and parsed['status'] != False):
            filteredEvent = [event for event in parsed if "2261" in event['teryt']]
            
            for event in filteredEvent:            
                self.weatherWarning.append(event['tresc'])   
        logger.info("Received " + str(len(self.weatherWarning)) + " warnings.")

    def PrintWarnings(self):   
        for warning in self.weatherWarning:
            print(warning)
            print('//////////')

    def DrawWarnings(self,draw:ImageDraw.ImageDraw,fonts,x1:int,y1:int,x2:int,y2:int):
        if len(self.weatherWarning) == 0:
            draw.text((x1+5,y1+8),"• Brak ostrzeżeń",0,fonts['font18light'])
        elif len(self.weatherWarning) == 1:
            wrappedText = imageHelper.WrappedText('• '+self.weatherWarning[0],fonts['font18light'],x2-x1-10)
            draw.text((x1+5,y1+8),wrappedText,0,fonts['font18light'])
        elif len(self.weatherWarning) >= 1:
            for warning in self.weatherWarning:
                wrappedText = imageHelper.WrappedText('• '+warning,fonts['font14light'],x2-x1-10)
                draw.text((x1+5,y1+8),wrappedText,0,fonts['font14light'])
    

if __name__ == "__main__":
    myWarnings = WeatherWarnings()
    myWarnings.PrintWarnings()