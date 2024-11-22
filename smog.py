import requests
import urllib3
import json
from PIL import Image,ImageDraw,ImageFont
import imageHelper

class Smog:
    Smog25 = ''
    Smog10 = ''
    def __init__(self) -> None:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get('https://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/736',verify=False)
        parsed = response.json()
        self.Smog10 = parsed['pm10IndexLevel']['indexLevelName']
        self.Smog25 = parsed['pm25IndexLevel']['indexLevelName']
        
    def PrintSmog(self):   
        print('Pył PM 2.5: ',self.Smog25)
        print('Pył PM 10: ',self.Smog10)

    def DrawSmog(self,draw:ImageDraw.ImageDraw,fonts,x1:int,y1:int,x2:int,y2:int):
        draw.text((x1,y1+9),"Pył PM 2.5: ",fill=0,font=fonts['font14light'])
        draw.text((x1,y1+24),self.Smog25,fill=0,font=fonts['font14'])


        draw.text((x1,y1+51),"Pył PM 10: ",fill=0,font=fonts['font14light'])
        draw.text((x1,y1+66),self.Smog10,fill=0,font=fonts['font14'])

        imageHelper.DrawDottedVerticalLine(draw,x1-15,y1,y2,4)
