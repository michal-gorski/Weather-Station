import requests
from bs4 import BeautifulSoup
import urllib3
from PIL import Image, ImageDraw, ImageFont
import imageHelper
import re


class Forecast:
    forecast = {}
    hourForecast = {}
    icons = {
        "Mostly Cloudy": "mostly_cloudy",
        "Partly Cloudy Night": "partly_cloudy_night",
        "Scattered Showers Night": "scattered_showers_night",
        "Scattered Showers": "scattered_showers",
        "Partly Cloudy": "partly_cloudy",
        "Sunny": "sunny",
        "Rain and Snow": "rain_and_snow",
        "Snow": "snow",
        "Cloudy": "cloudy",
        "Rain": "rain",
        "Mostly Cloudy Night": "mostly_cloudy_night",
        "Scattered Snow Night": "scattered_snow_night",
        "Clear Night": "clear_night",
        "Mostly Sunny": "mostly_sunny",
        "Mostly Clear Night": "mostly_clear_night",
        "Foggy":'foggy'
    }

    def __init__(
        self,
        url="https://weather.com/pl-PL/weather/tenday/l/93409ef628e2eccc8fe84493beb24470c722d12ef4632a9c49250af345ba81ef",
    ):
        try:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            response = requests.get(url, verify=False)
            soup = BeautifulSoup(response.text, "html.parser")
            mydivs = soup.find_all("div")

            filteredDivs = []
            for div in mydivs:
                testId = div.get("data-testid")
                if testId == "DailyContent":
                    filteredDivs.append(div)

            for div in filteredDivs:
                day = div.h2.text.split("|")[0].strip()
                dayPart = div.h2.text.split("|")[1].strip()
                if day not in self.forecast:
                    self.forecast[day] = dict()
                self.forecast[day][dayPart] = dict()
                self.forecast[day][dayPart]["temperature"] = div.find_all(
                    attrs={"data-testid": "TemperatureValue"}
                )[0].text
                self.forecast[day][dayPart]["wind"] = div.find_all(
                    attrs={"data-testid": "Wind"}
                )[0].text.replace("\xa0", " ")
                self.forecast[day][dayPart]["rain"] = div.find_all(
                    attrs={"data-testid": "PercentageValue"}
                )[0].text.replace("\xa0", " ")
                self.forecast[day][dayPart]["icon"] = div.find_all(
                    attrs={"data-testid": "weatherIcon"}
                )[0].text

            url = "https://weather.com/pl-PL/pogoda/godzinowa/l/93409ef628e2eccc8fe84493beb24470c722d12ef4632a9c49250af345ba81ef"
            response = requests.get(url, verify=False)
            soup = BeautifulSoup(response.text, "html.parser")
            mydivs = soup.find_all("div")

            filteredDivs = []
            for div in mydivs:
                testId = div.get("data-testid")
                if testId == "DetailsSummary":
                    filteredDivs.append(div)

            for div in filteredDivs:
                hour = div.h2.text
                self.hourForecast[hour] = dict()
                self.hourForecast[hour]["temperature"] = div.find_all(
                    attrs={"data-testid": "TemperatureValue"}
                )[0].text
                self.hourForecast[hour]["wind"] = div.find_all(
                    attrs={"data-testid": "Wind"}
                )[0].text.replace("\xa0", " ")
                self.hourForecast[hour]["rain"] = div.find_all(
                    attrs={"data-testid": "PercentageValue"}
                )[0].text.replace("\xa0", " ")
                self.hourForecast[hour]["icon"] = div.find_all(
                    attrs={"data-testid": "Icon"}
                )[0].text

        except:
            print("Exception loading forecast")

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

            if skipFirst != True and position <= 6:
                leftBorder = x1 + round(position * (x2 - x1) / 7)
                boxWidth = round((x2 - x1) / 7)

                # draw box line
                imageHelper.DrawDottedVerticalLine(
                    draw, leftBorder + boxWidth, y1, y2, 4
                )

                # draw day title
                dayTextLen = draw.textlength(
                    forecastDay, font=fonts["font14"], direction=None, features=None
                )
                dayTextPos = round(leftBorder + boxWidth / 2 - dayTextLen / 2)
                draw.text((dayTextPos, y1 + 5), forecastDay, 0, font=fonts["font14"])

                # draw weather icon
                iconName = (
                    self.icons[self.forecast[forecastDay]["Dzień"]["icon"]] + "_small"
                )
                iconWidth = icons[iconName].width
                draw._image.paste(
                    icons[iconName],
                    (leftBorder + 5 + round((70 - iconWidth) / 2), y1 + 23),
                )

                # draw temperature
                temperature = (
                    self.forecast[forecastDay]["Dzień"]["temperature"]
                    + " / "
                    + self.forecast[forecastDay]["Noc"]["temperature"]
                )
                tempTextLen = draw.textlength(
                    temperature, font=fonts["font18"], direction=None, features=None
                )
                tempTextPos = round(leftBorder + boxWidth / 2 - tempTextLen / 2)
                draw.text((tempTextPos, y1 + 61), temperature, 0, font=fonts["font18"])

                # draw wind
                wind = (
                    re.findall(r"\d+", self.forecast[forecastDay]["Dzień"]["wind"])[0]
                    + " km/h"
                )
                windTextLen = draw.textlength(
                    wind, font=fonts["font14light"], direction=None, features=None
                )
                windTextPos = round(leftBorder + boxWidth / 2 - windTextLen / 2)
                draw.text((windTextPos, y1 + 80), wind, 0, font=fonts["font14light"])

                position += 1

            elif skipFirst == True:
                skipFirst = False

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

                # draw hour title
                dayTextLen = draw.textlength(
                    forecastHour, font=fonts["font14"], direction=None, features=None
                )
                dayTextPos = round(leftBorder + boxWidth / 2 - dayTextLen / 2)
                draw.text((dayTextPos, y1 + 5), forecastHour, 0, font=fonts["font14"])

                # draw weather icon
                iconName = (
                    self.icons[self.hourForecast[forecastHour]["icon"]] + "_small"
                )
                iconWidth = icons[iconName].width
                draw._image.paste(
                    icons[iconName], (leftBorder + round((70 - iconWidth) / 2), y1 + 25)
                )

                # draw temperature
                temperature = self.hourForecast[forecastHour]["temperature"]
                tempTextLen = draw.textlength(
                    temperature, font=fonts["font18"], direction=None, features=None
                )
                tempTextPos = round(leftBorder + boxWidth / 2 - tempTextLen / 2)
                draw.text((tempTextPos+2, y1 + 63), temperature, 0, font=fonts["font18"])

                # draw wind
                wind = (
                    re.findall(r"\d+", self.hourForecast[forecastHour]["wind"])[0]
                    + " km/h"
                )
                windTextLen = draw.textlength(
                    wind, font=fonts["font14light"], direction=None, features=None
                )
                windTextPos = round(leftBorder + boxWidth / 2 - windTextLen / 2)
                draw.text((windTextPos, y1 + 88), wind, 0, font=fonts["font14light"])

                # draw wind icon
                if (
                    int(re.findall(r"\d+", self.hourForecast[forecastHour]["wind"])[0])
                    > 15
                ):
                    iconName = "wind_small"
                    iconWidth = icons[iconName].width
                    draw._image.paste(
                        icons[iconName],
                        (leftBorder + round((70 - iconWidth) / 2), y1 + 106),
                    )

                # draw rain
                rain = self.hourForecast[forecastHour]["rain"]
                tempTextLen = draw.textlength(
                    rain, font=fonts["font18"], direction=None, features=None
                )
                tempTextPos = round(leftBorder + boxWidth / 2 - tempTextLen / 2)
                draw.text((tempTextPos + 1, y1 + 136), rain, 0, font=fonts["font14"])

                # draw rain icon
                if (
                    int(re.findall(r"\d+", self.hourForecast[forecastHour]["rain"])[0])
                    > 25
                ):
                    iconName = "rain_percent_small"
                    iconWidth = icons[iconName].width
                    draw._image.paste(
                        icons[iconName],
                        (leftBorder + round((70 - iconWidth) / 2 - 6), y1 + 157),
                    )

                position += 1
