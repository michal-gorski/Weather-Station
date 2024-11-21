import requests
import urllib3
import json

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

    def DrawSmog(self,draw:ImageDraw.ImageDraw,fonts,icons,x1:int,y1:int,x2:int,y2:int):
        pass
