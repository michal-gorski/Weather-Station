import plotter
import clock
import schoolPlan
import weatherWarnings
import smog
import forecast
import datetime
import sensor
import asyncio
import logging

class WeatherStation:
    
    myForecast = None
    
    def __init__(self) -> None:
        pass

    async def RunWeatherStation(self):        
        
        self.mySensor = sensor.Sensor()

        await self.mySensor.Connect()

        self.myPlotter = plotter.Plotter(800, 480)
        
        self.myPlotter.EpdInit()

        currentMinute = 0
        while True:
            if datetime.datetime.now().minute != currentMinute:

                currentMinute = datetime.datetime.now().minute

                # Get data
                if self.myForecast == None or currentMinute % 10 == 0:
                    self.myForecast = forecast.Forecast()                
                    self.mySmog = smog.Smog()
                    self.myWarnings = weatherWarnings.WeatherWarnings()
                    self.myPlan = schoolPlan.SchoolPlan()
                    self.myPlan.CurrentPlan()

                self.myClock = clock.Clock()

                # sensor data
                if self.mySensor.connected:
                    await self.mySensor.GetData()
                    

                # draw data
                logger.info("Starting redraw")
                self.myPlotter.PrepareGrid()

                self.myPlan.DrawPlan(
                    self.myPlotter.draw,
                    self.myPlotter.fonts,
                    0,
                    self.myPlotter.firstHorizontal,
                    self.myPlotter.firstVertical,
                    self.myPlotter.height,
                )
                self.myClock.DrawClock(
                    self.myPlotter.draw,
                    self.myPlotter.fonts,
                    self.myPlotter.secondVertical,
                    0,
                    self.myPlotter.width,
                    self.myPlotter.firstHorizontal,
                )
                self.myForecast.DrawForecast(
                    self.myPlotter.draw,
                    self.myPlotter.fonts,
                    self.myPlotter.icons,
                    self.myPlotter.firstVertical,
                    self.myPlotter.fourthHorizontal,
                    self.myPlotter.width - 12,
                    self.myPlotter.height,
                )
                self.myForecast.DrawHourly(
                    self.myPlotter.draw,
                    self.myPlotter.fonts,
                    self.myPlotter.icons,
                    self.myPlotter.firstVertical,
                    self.myPlotter.firstHorizontal,
                    self.myPlotter.width - 12,
                    self.myPlotter.thirdHorizontal,
                )
                self.myWarnings.DrawWarnings(
                    self.myPlotter.draw,
                    self.myPlotter.fonts,
                    self.myPlotter.firstVertical,
                    self.myPlotter.thirdHorizontal,
                    self.myPlotter.width,
                    self.myPlotter.fourthHorizontal,
                )
                self.mySmog.DrawSmog(
                    self.myPlotter.draw,
                    self.myPlotter.fonts,
                    self.myPlotter.secondVertical - 100,
                    0,
                    self.myPlotter.secondVertical,
                    self.myPlotter.firstHorizontal,
                )

                self.mySensor.DrawSensor(
                    self.myPlotter.draw,
                    self.myPlotter.fonts,
                    0,
                    0,
                    self.myPlotter.secondVertical - 100,
                    self.myPlotter.firstHorizontal,
                )

                if self.myPlotter.epdReady == True:
                    self.myPlotter.Display()
                else:
                    self.myPlotter.ShowImage()
            
if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("weatherstation.log"),
            logging.StreamHandler()
        ]
    )


    try:
        weatherStation = WeatherStation()
        asyncio.run(weatherStation.RunWeatherStation())
    
    except KeyboardInterrupt:
        weatherStation.myPlotter.EpdSleep()
        if weatherStation.mySensor.connected:
            weatherStation.mySensor.Disconnect()