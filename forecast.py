import requests
import urllib3
from PIL import Image, ImageDraw, ImageFont
import imageHelper
import re
import logging
from datetime import datetime
logger = logging.getLogger(__name__)

class Forecast:
    forecast = {}
    hourForecast = {}
    icons = {     
        "Clear Night":"clear_night",
        "Partly Cloudy Night":"partly_cloudy_night",
        "Cloudy Night":"mostly_cloudy_night",
        "Overcast Night":"cloudy",
        "Mist Night":"foggy",
        "Patchy rain nearby Night":"scattered_showers_night",
        "Patchy rain possible Night":"scattered_showers_night",
        "Patchy snow possible Night":"scattered_snow_night",
        "Patchy sleet possible Night":"foggy",
        "Patchy freezing drizzle possible Night":"rain_and_snow",
        "Thundery outbreaks possible Night":"thunder",
        "Blowing snow Night":"snow",
        "Blizzard Night":"snow",
        "Fog Night":"foggy",
        "Freezing fog Night":"foggy",
        "Patchy light drizzle Night":"scattered_showers",
        "Light drizzle Night":"scattered_showers",
        "Freezing drizzle Night":"rain_and_snow",
        "Heavy freezing drizzle Night":"rain_and_snow",
        "Patchy light rain Night":"scattered_showers",
        "Light rain Night":"showers",
        "Moderate rain at times Night":"showers",
        "Moderate rain Night":"rain",
        "Heavy rain at times Night":"rain",
        "Heavy rain Night":"heavy_rain",
        "Light freezing rain Night":"rain_and_snow",
        "Moderate or heavy freezing rain Night":"rain_and_snow",
        "Light sleet Night":"foggy",
        "Moderate or heavy sleet Night":"foggy",
        "Patchy light snow Night":"snow",
        "Light snow Night":"snow",
        "Patchy moderate snow Night":"snow",
        "Moderate snow Night":"snow",
        "Patchy heavy snow Night":"heavy_snow",
        "Heavy snow Night":"heavy_snow",
        "Ice pellets Night":"hail",
        "Light rain shower Night":"scattered_showers",
        "Moderate or heavy rain shower Night":"showers",
        "Torrential rain shower Night":"rain",
        "Light sleet showers Night":"scattered_showers",
        "Moderate or heavy sleet showers Night":"showers",
        "Light snow showers Night":"snow",
        "Moderate or heavy snow showers Night":"heavy_snow",
        "Light showers of ice pellets Night":"hail",
        "Moderate or heavy showers of ice pellets Night":"hail",
        "Patchy light rain with thunde Night":"thunder",
        "Moderate or heavy rain with thunder Night":"thunder",
        "Patchy light snow with thunder Night":"thunder",
        "Moderate or heavy snow with thunder Night":"thunder",
        "Sunny":"sunny",
        "Partly Cloudy":"partly_cloudy",
        "Cloudy":"mostly_cloudy",
        "Overcast":"cloudy",
        "Mist":"foggy",
        "Patchy rain possible":"showers",
        "Patchy snow possible":"snow",
        "Patchy sleet possible":"foggy",
        "Patchy freezing drizzle possible":"rain_and_snow",
        "Thundery outbreaks possible":"thunder",
        "Blowing snow":"snow",
        "Blizzard":"snow",
        "Fog":"foggy",
        "Freezing fog":"foggy",
        "Patchy light drizzle":"scattered_showers",
        "Light drizzle":"scattered_showers",
        "Freezing drizzle":"rain_and_snow",
        "Heavy freezing drizzle":"rain_and_snow",
        "Patchy light rain":"scattered_showers",
        "Light rain":"showers",
        "Moderate rain at times":"showers",
        "Moderate rain":"rain",
        "Heavy rain at times":"rain",
        "Heavy rain":"heavy_rain",
        "Light freezing rain":"rain_and_snow",
        "Moderate or heavy freezing rain":"rain_and_snow",
        "Light sleet":"foggy",
        "Moderate or heavy sleet":"foggy",
        "Patchy light snow":"snow",
        "Light snow":"snow",
        "Patchy moderate snow":"snow",
        "Moderate snow":"snow",
        "Patchy heavy snow":"heavy_snow",
        "Heavy snow":"heavy_snow",
        "Ice pellets":"hail",
        "Light rain shower":"scattered_showers",
        "Moderate or heavy rain shower":"showers",
        "Torrential rain shower":"rain",
        "Light sleet showers":"scattered_showers",
        "Moderate or heavy sleet showers":"showers",
        "Light snow showers":"snow",
        "Moderate or heavy snow showers":"heavy_snow",
        "Light showers of ice pellets":"hail",
        "Moderate or heavy showers of ice pellets":"hail",
        "Patchy light rain with thunder":"thunder",
        "Moderate or heavy rain with thunder":"thunder",
        "Patchy light snow with thunder":"thunder",
        "Moderate or heavy snow with thunder":"thunder"
    }

    def __init__(
        self,
        url="http://api.weatherapi.com/v1/forecast.json?key=6f5d0f74d85f4293a1c155846252811&q=Gdansk&days=7&aqi=no&alerts=no"):
        try:
            logger.info("Getting forecast")
            self.forecast = {}
            self.hourForecast = {}
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            response = requests.get(url, verify=False)
            # Extract daily forecast
            forecast_days = response.json()["forecast"]["forecastday"]

            for day in forecast_days:
                date = day["date"]
                self.forecast[date] = dict()
                self.forecast[date]["temperatureMax"] = day["day"]["maxtemp_c"]
                self.forecast[date]["temperatureMin"] = day["day"]["mintemp_c"]

                self.forecast[date]["wind"] = day["day"]["maxwind_kph"]
                self.forecast[date]["rain"] = day["day"]["totalprecip_mm"]
                self.forecast[date]["icon"] = day["day"]["condition"]["text"].strip()
                
            #extract hourly forecast
            forecast_hours = response.json()["forecast"]["forecastday"][0]["hour"]
            hoursCount = 0
            for hour in forecast_hours:
                forecastHour = hour["time"]
                 
                # Convert string to datetime object
                target_time = datetime.strptime(forecastHour, "%Y-%m-%d %H:%M")

                # Get current time
                current_time = datetime.now()

                # Compare
                if target_time > current_time and hoursCount < 10:
                    hoursCount+=1
                    self.hourForecast[forecastHour] = dict()
                    self.hourForecast[forecastHour]["temperature"] = hour["temp_c"]
                    self.hourForecast[forecastHour]["wind"] = hour["wind_kph"]
                    self.hourForecast[forecastHour]["rain"] = hour["precip_mm"]
                    self.hourForecast[forecastHour]["icon"] = hour["condition"]["text"]
                    if (hour["is_day"] == 0):
                        self.hourForecast[forecastHour]['icon'] = f"{self.hourForecast[forecastHour]['icon']}".strip() + " Night"
            
        except Exception as e:
            logger.info("Exception loading forecast: " + str(e))

    def PrintForecast(self):
        for forecastDay in self.forecast:
            for dayPart in self.forecast[forecastDay]:
                print(
                    forecastDay,
                    " | ",
                    dayPart,
                    ": temperatura: ",
                    self.forecast[forecastDay][dayPart]["temperature"],
                    " | wiatr: ",
                    self.forecast[forecastDay][dayPart]["wind"],
                    " | deszcz: ",
                    self.forecast[forecastDay][dayPart]["rain"],
                    " | opis: ",
                    self.forecast[forecastDay][dayPart]["icon"],
                    ":",
                    self.icons[self.forecast[forecastDay][dayPart]["icon"]],
                )
                print("-------")

    def DrawForecast(
        self,
        draw: ImageDraw.ImageDraw,
        fonts,
        icons,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
    ):
        position = 0
        skipFirst = True

        if len(self.forecast) == 0:
            raise Exception("No loaded forecast")

        for forecastDay in self.forecast:

            if position <= 7:
                leftBorder = x1 + round(position * (x2 - x1) / 7)
                boxWidth = round((x2 - x1) / 7)

                # draw box line
                imageHelper.DrawDottedVerticalLine(
                    draw, leftBorder + boxWidth, y1, y2, 4
                )

                # draw day title
                forecastTemp = datetime.strptime(forecastDay, "%Y-%m-%d")

                # Polish weekday abbreviations (Mon=0 ... Sun=6)
                polish_weekdays = ["Pon", "Wt", "Śr", "Czw", "Pt", "Sob", "Nie"]

                # Construct the string
                dayText = f"{polish_weekdays[forecastTemp.weekday()]}. {forecastTemp.day}"

                dayTextLen = draw.textlength(
                    dayText, font=fonts["font14"], direction=None, features=None
                )
                dayTextPos = round(leftBorder + boxWidth / 2 - dayTextLen / 2)
                draw.text((dayTextPos, y1 + 5), dayText, 0, font=fonts["font14"])

                forecastName = self.forecast[forecastDay]["icon"]
                # draw weather icon
                iconName = (                    
                    self.icons[forecastName]+ "_small"
                )
                iconWidth = icons[iconName].width
                draw._image.paste(
                    icons[iconName],
                    (leftBorder + 5 + round((70 - iconWidth) / 2), y1 + 23),
                )

                # draw temperature
                temperature = f"{self.forecast[forecastDay]['temperatureMax']}° / {self.forecast[forecastDay]['temperatureMin']}°"
        
                tempTextLen = draw.textlength(
                    temperature, font=fonts["font18"], direction=None, features=None
                )
                tempTextPos = round(leftBorder + boxWidth / 2 - tempTextLen / 2)
                draw.text((tempTextPos, y1 + 61), temperature, 0, font=fonts["font18"])

                # draw wind
                wind = f"{self.forecast[forecastDay]['wind']} km/h"
                
                windTextLen = draw.textlength(
                    wind, font=fonts["font14light"], direction=None, features=None
                )
                windTextPos = round(leftBorder + boxWidth / 2 - windTextLen / 2)
                draw.text((windTextPos, y1 + 80), wind, 0, font=fonts["font14light"])

                position += 1

            
            
    def DrawHourly(
        self,
        draw: ImageDraw.ImageDraw,
        fonts,
        icons,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
    ):
        position = 0
        if len(self.forecast) == 0:
            raise Exception("No loaded forecast")

        for forecastHour in self.hourForecast:

            if position <= 8:
                leftBorder = x1 + round(position * (x2 - x1) / 9)
                boxWidth = round((x2 - x1) / 9)

                # draw box line
                imageHelper.DrawDottedVerticalLine(
                    draw, leftBorder + boxWidth, y1, y2, 4
                )

                # Convert string to datetime object
                date_obj = datetime.strptime(forecastHour, "%Y-%m-%d %H:%M")

                # Extract only the time
                hourText = f"{date_obj.time()}"[0:5]

                # draw hour title
                dayTextLen = draw.textlength(
                    hourText, font=fonts["font14"], direction=None, features=None
                )
                dayTextPos = round(leftBorder + boxWidth / 2 - dayTextLen / 2)
                draw.text((dayTextPos, y1 + 5), hourText, 0, font=fonts["font14"])

                # draw weather icon
                iconName = (
                    self.icons[self.hourForecast[forecastHour]["icon"].strip()] + "_small"
                )
                iconWidth = icons[iconName].width
                draw._image.paste(
                    icons[iconName], (leftBorder + round((70 - iconWidth) / 2), y1 + 25)
                )

                # draw temperature
                temperature = f"{round(self.hourForecast[forecastHour]["temperature"])}°"
                tempTextLen = draw.textlength(
                    temperature, font=fonts["font18"], direction=None, features=None
                )
                tempTextPos = round(leftBorder + boxWidth / 2 - tempTextLen / 2)
                draw.text((tempTextPos+2, y1 + 63), temperature, 0, font=fonts["font18"])

                # draw wind
                wind = f"{round(self.hourForecast[forecastHour]['wind'])} km/h"
                
                windTextLen = draw.textlength(
                    wind, font=fonts["font14light"], direction=None, features=None
                )
                windTextPos = round(leftBorder + boxWidth / 2 - windTextLen / 2)
                draw.text((windTextPos, y1 + 88), wind, 0, font=fonts["font14light"])

                # draw wind icon
                if (
                    int(self.hourForecast[forecastHour]["wind"]) > 15
                ):
                    iconName = "wind_small"
                    iconWidth = icons[iconName].width
                    draw._image.paste(
                        icons[iconName],
                        (leftBorder + round((70 - iconWidth) / 2), y1 + 106),
                    )

                # draw rain
                rain = f"{self.hourForecast[forecastHour]['rain']}mm"
                tempTextLen = draw.textlength(
                    rain, font=fonts["font18"], direction=None, features=None
                )
                tempTextPos = round(leftBorder + boxWidth / 2 - tempTextLen / 2)
                draw.text((tempTextPos + 3, y1 + 138), rain, 0, font=fonts["font14"])

                # draw rain icon
                if (int(self.hourForecast[forecastHour]["rain"]) > 25):
                    iconName = "rain_percent_small"
                    iconWidth = icons[iconName].width
                    draw._image.paste(
                        icons[iconName],
                        (leftBorder + round((70 - iconWidth) / 2 - 6), y1 + 157),
                    )

                position += 1
