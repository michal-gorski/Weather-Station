import requests
import urllib3
import json



class WeatherWarnings:
    weatherWarning = []
    def __init__(self) -> None:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get('https://danepubliczne.imgw.pl/api/data/warningsmeteo',verify=False)
        parsed = response.json()
        filteredEvent = [event for event in parsed if "2261" in event['teryt']]
        
        for event in filteredEvent:            
            self.weatherWarning.append(event['tresc'])
             
        
        
    def PrintWarnings(self):   
        for warning in self.weatherWarning:
            print(warning)
            print('//////////')
