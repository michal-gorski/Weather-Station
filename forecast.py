import requests
from PIL import Image, ImageDraw, ImageFont
import imageHelper
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)

class Forecast:
    # Configuration constants
    OPEN_METEO_API_URL = "https://api.open-meteo.com/v1/forecast"
    LATITUDE = 54.352  # Gdansk
    LONGITUDE = 18.6466
    TIMEZONE = "Europe/Warsaw"
    HOURLY_FORECAST_LIMIT = 10
    MAX_DAILY_FORECASTS = 7
    WIND_SPEED_THRESHOLD = 15  # km/h
    RAIN_PERCENTAGE_THRESHOLD = 25

    # WMO weather interpretation codes -> (day icon, night icon)
    # https://open-meteo.com/en/docs#weather_variable_documentation
    icons = {
        0: ("sunny", "clear_night"),  # Clear sky
        1: ("mostly_sunny", "mostly_clear_night"),  # Mainly clear
        2: ("partly_cloudy", "partly_cloudy_night"),  # Partly cloudy
        3: ("cloudy", "cloudy"),  # Overcast
        45: ("foggy", "foggy"),  # Fog
        48: ("foggy", "foggy"),  # Depositing rime fog
        51: ("scattered_showers", "scattered_showers_night"),  # Light drizzle
        53: ("scattered_showers", "scattered_showers_night"),  # Moderate drizzle
        55: ("showers", "showers"),  # Dense drizzle
        56: ("rain_and_snow", "rain_and_snow"),  # Light freezing drizzle
        57: ("rain_and_snow", "rain_and_snow"),  # Dense freezing drizzle
        61: ("showers", "showers"),  # Slight rain
        63: ("rain", "rain"),  # Moderate rain
        65: ("heavy_rain", "heavy_rain"),  # Heavy rain
        66: ("rain_and_snow", "rain_and_snow"),  # Light freezing rain
        67: ("rain_and_snow", "rain_and_snow"),  # Heavy freezing rain
        71: ("snow", "snow"),  # Slight snow fall
        73: ("snow", "snow"),  # Moderate snow fall
        75: ("heavy_snow", "heavy_snow"),  # Heavy snow fall
        77: ("snow", "snow"),  # Snow grains
        80: ("scattered_showers", "scattered_showers_night"),  # Slight rain showers
        81: ("showers", "showers"),  # Moderate rain showers
        82: ("heavy_rain", "heavy_rain"),  # Violent rain showers
        85: ("snow", "snow"),  # Slight snow showers
        86: ("heavy_snow", "heavy_snow"),  # Heavy snow showers
        95: ("thunder", "thunder"),  # Thunderstorm
        96: ("hail", "hail"),  # Thunderstorm with slight hail
        99: ("hail", "hail"),  # Thunderstorm with heavy hail
    }
    DEFAULT_ICON = "cloudy"

    WIND_DIRECTIONS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

    def __init__(self):
        self.forecast = {}
        self.hourForecast = {}
        self.GetForecastOpenMeteo()

    def IconName(self, weatherCode, isDay=True):
        dayIcon, nightIcon = self.icons.get(int(weatherCode), (self.DEFAULT_ICON, self.DEFAULT_ICON))
        return dayIcon if isDay else nightIcon

    def WindDirection(self, degrees):
        return self.WIND_DIRECTIONS[round(degrees / 45) % 8]

    def GetForecastOpenMeteo(self):
        params = {
            "latitude": self.LATITUDE,
            "longitude": self.LONGITUDE,
            "timezone": self.TIMEZONE,
            "forecast_days": self.MAX_DAILY_FORECASTS,
            # +1 because the current, already started hour is skipped below
            "forecast_hours": self.HOURLY_FORECAST_LIMIT + 1,
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,"
                     "wind_speed_10m_max,wind_direction_10m_dominant,precipitation_sum",
            "hourly": "temperature_2m,weather_code,wind_speed_10m,precipitation,"
                      "precipitation_probability,is_day",
        }
        try:
            logger.info("Getting forecast")
            response = requests.get(self.OPEN_METEO_API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            daily = data["daily"]
            for i, date in enumerate(daily["time"]):
                self.forecast[date] = dict()
                self.forecast[date]["temperatureMax"] = daily["temperature_2m_max"][i]
                self.forecast[date]["temperatureMin"] = daily["temperature_2m_min"][i]
                self.forecast[date]["wind"] = f"{round(daily['wind_speed_10m_max'][i])}{self.WindDirection(daily['wind_direction_10m_dominant'][i])}"
                self.forecast[date]["rain"] = daily["precipitation_sum"][i]
                self.forecast[date]["icon"] = self.IconName(daily["weather_code"][i])

            # Open-Meteo returns naive local times for the requested timezone
            current_time = datetime.now(ZoneInfo(self.TIMEZONE)).replace(tzinfo=None)

            hourly = data["hourly"]
            for i, forecastHour in enumerate(hourly["time"]):
                if datetime.fromisoformat(forecastHour) <= current_time:
                    continue
                if len(self.hourForecast) >= self.HOURLY_FORECAST_LIMIT:
                    break
                self.hourForecast[forecastHour] = dict()
                self.hourForecast[forecastHour]["temperature"] = hourly["temperature_2m"][i]
                self.hourForecast[forecastHour]["wind"] = hourly["wind_speed_10m"][i]
                self.hourForecast[forecastHour]["rain"] = hourly["precipitation"][i]
                self.hourForecast[forecastHour]["rainProbability"] = hourly["precipitation_probability"][i] or 0
                self.hourForecast[forecastHour]["icon"] = self.IconName(hourly["weather_code"][i], hourly["is_day"][i] == 1)

            logger.info(f"Forecast collected: {len(self.forecast)} days, {len(self.hourForecast)} hours")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching Open-Meteo forecast: {e}")
        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"Error parsing Open-Meteo response: {e}")

    def PrintForecast(self):
        for forecastDay, day in self.forecast.items():
            print(
                forecastDay,
                " | temperatura: ", day["temperatureMax"], "/", day["temperatureMin"],
                " | wiatr: ", day["wind"],
                " | deszcz: ", day["rain"],
                " | ikona: ", day["icon"],
            )
        print("-------")
        for forecastHour, hour in self.hourForecast.items():
            print(
                forecastHour,
                " | temperatura: ", hour["temperature"],
                " | wiatr: ", hour["wind"],
                " | deszcz: ", hour["rain"], "mm (", hour["rainProbability"], "%)",
                " | ikona: ", hour["icon"],
            )

    def DrawNoForecast(self, draw: ImageDraw.ImageDraw, fonts, x1: int, y1: int):
        draw.text((x1 + 5, y1 + 8), "• Brak prognozy", 0, fonts["font18light"])

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
        if len(self.forecast) == 0:
            self.DrawNoForecast(draw, fonts, x1, y1)
            return

        # Polish weekday abbreviations (Mon=0 ... Sun=6)
        polish_weekdays = ["Pon", "Wt", "Śr", "Czw", "Pt", "Sob", "Nie"]
        boxWidth = round((x2 - x1) / self.MAX_DAILY_FORECASTS)

        for position, forecastDay in enumerate(self.forecast):
            if position >= self.MAX_DAILY_FORECASTS:
                break
            day = self.forecast[forecastDay]
            leftBorder = x1 + round(position * (x2 - x1) / self.MAX_DAILY_FORECASTS)

            # draw box line
            imageHelper.DrawDottedVerticalLine(
                draw, leftBorder + boxWidth, y1, y2, 4
            )

            # draw day title
            forecastDate = datetime.strptime(forecastDay[0:10], "%Y-%m-%d")
            dayText = f"{polish_weekdays[forecastDate.weekday()]}. {forecastDate.day}"

            dayTextLen = draw.textlength(dayText, font=fonts["font14"])
            dayTextPos = round(leftBorder + boxWidth / 2 - dayTextLen / 2)
            draw.text((dayTextPos, y1 + 5), dayText, 0, font=fonts["font14"])

            # draw weather icon
            icon = icons[day["icon"] + "_small"]
            draw._image.paste(
                icon,
                (leftBorder + round((boxWidth - icon.width) / 2), y1 + 23),
            )

            # draw temperature
            temperature = f"{round(day['temperatureMax'])}° / {round(day['temperatureMin'])}°"
            tempTextLen = draw.textlength(temperature, font=fonts["font18"])
            tempTextPos = round(leftBorder + boxWidth / 2 - tempTextLen / 2)
            draw.text((tempTextPos, y1 + 61), temperature, 0, font=fonts["font18"])

            # draw wind
            wind = f"{day['wind']} km/h"
            windTextLen = draw.textlength(wind, font=fonts["font14light"])
            windTextPos = round(leftBorder + boxWidth / 2 - windTextLen / 2)
            draw.text((windTextPos, y1 + 80), wind, 0, font=fonts["font14light"])

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
        if len(self.hourForecast) == 0:
            self.DrawNoForecast(draw, fonts, x1, y1)
            return

        hourly_slots = self.HOURLY_FORECAST_LIMIT - 1
        boxWidth = round((x2 - x1) / hourly_slots)

        for position, forecastHour in enumerate(self.hourForecast):
            if position >= hourly_slots:
                break
            hour = self.hourForecast[forecastHour]
            leftBorder = x1 + round(position * (x2 - x1) / hourly_slots)

            # draw box line
            imageHelper.DrawDottedVerticalLine(
                draw, leftBorder + boxWidth, y1, y2, 4
            )

            # draw hour title
            hourText = datetime.fromisoformat(forecastHour).strftime("%H:%M")
            hourTextLen = draw.textlength(hourText, font=fonts["font14"])
            hourTextPos = round(leftBorder + boxWidth / 2 - hourTextLen / 2)
            draw.text((hourTextPos, y1 + 5), hourText, 0, font=fonts["font14"])

            # draw weather icon
            icon = icons[hour["icon"] + "_small"]
            draw._image.paste(
                icon, (leftBorder + round((boxWidth - icon.width) / 2), y1 + 25)
            )

            # draw temperature
            temperature = f"{round(hour['temperature'])}°"
            tempTextLen = draw.textlength(temperature, font=fonts["font18"])
            tempTextPos = round(leftBorder + boxWidth / 2 - tempTextLen / 2)
            draw.text((tempTextPos + 2, y1 + 63), temperature, 0, font=fonts["font18"])

            # draw wind
            wind = f"{round(hour['wind'])} km/h"
            windTextLen = draw.textlength(wind, font=fonts["font14light"])
            windTextPos = round(leftBorder + boxWidth / 2 - windTextLen / 2)
            draw.text((windTextPos, y1 + 88), wind, 0, font=fonts["font14light"])

            # draw wind icon
            if hour["wind"] > self.WIND_SPEED_THRESHOLD:
                icon = icons["wind_small"]
                draw._image.paste(
                    icon,
                    (leftBorder + round((boxWidth - icon.width) / 2), y1 + 106),
                )

            # draw rain
            rain = f"{hour['rain']:.1f}mm"
            rainTextLen = draw.textlength(rain, font=fonts["font14"])
            rainTextPos = round(leftBorder + boxWidth / 2 - rainTextLen / 2)
            draw.text((rainTextPos, y1 + 138), rain, 0, font=fonts["font14"])

            # draw rain icon when rain is likely
            if hour["rainProbability"] > self.RAIN_PERCENTAGE_THRESHOLD:
                icon = icons["rain_percent_small"]
                draw._image.paste(
                    icon,
                    (leftBorder + round((boxWidth - icon.width) / 2), y1 + 157),
                )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    Forecast().PrintForecast()
