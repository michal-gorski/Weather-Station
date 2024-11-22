import plotter
import clock
import schoolPlan
import weatherWarnings
import smog
import forecast
import logging
import datetime
import sensor
import asyncio


logger = logging.getLogger(__name__)

logging.basicConfig(filename="myapp.log", level=logging.INFO)
logger.info("Initializing...")


logger.info("Getting sensor data")
mySensor = sensor.Sensor()
if asyncio.run(mySensor.Connect()):
    asyncio.run(mySensor.GetData())
mySensor.PrintSensor()

logger.info("Initializing plotter")
myPlotter = plotter.Plotter(800, 480)

try:
    currentMinute = 0
    while True:
        if datetime.datetime.now().minute != currentMinute:

            currentMinute = datetime.datetime.now().minute

            # Get data
            logger.info("Getting forecast")
            myForecast = forecast.Forecast()
            myForecast.PrintForecast()

            logger.info("Getting Smog Data")
            mySmog = smog.Smog()
            mySmog.PrintSmog()

            logger.info("Getting Warnings Data")
            myWarnings = weatherWarnings.WeatherWarnings()
            myWarnings.PrintWarnings()

            logger.info("Getting school plan")
            myPlan = schoolPlan.SchoolPlan()
            myPlan.CurrentPlan()
            myPlan.PrintPlan()

            logger.info("Getting clock")
            myClock = clock.Clock()
            myClock.PrintClock()

            # sensor data
            if mySensor.connected:
                asyncio.run(mySensor.GetData())
                mySensor.PrintSensor()

            # draw data
            myPlotter.PrepareGrid()

            myPlan.DrawPlan(
                myPlotter.draw,
                myPlotter.fonts,
                0,
                myPlotter.firstHorizontal,
                myPlotter.firstVertical,
                myPlotter.height,
            )
            myClock.DrawClock(
                myPlotter.draw,
                myPlotter.fonts,
                myPlotter.secondVertical,
                0,
                myPlotter.width,
                myPlotter.firstHorizontal,
            )
            myForecast.DrawForecast(
                myPlotter.draw,
                myPlotter.fonts,
                myPlotter.icons,
                myPlotter.firstVertical,
                myPlotter.fourthHorizontal,
                myPlotter.width,
                myPlotter.height,
            )
            myForecast.DrawHourly(
                myPlotter.draw,
                myPlotter.fonts,
                myPlotter.icons,
                myPlotter.firstVertical,
                myPlotter.firstHorizontal,
                myPlotter.width,
                myPlotter.thirdHorizontal,
            )
            myWarnings.DrawWarnings(
                myPlotter.draw,
                myPlotter.fonts,
                myPlotter.firstVertical,
                myPlotter.thirdHorizontal,
                myPlotter.width,
                myPlotter.fourthHorizontal,
            )
            mySmog.DrawSmog(
                myPlotter.draw,
                myPlotter.fonts,
                myPlotter.secondVertical - 100,
                0,
                myPlotter.secondVertical,
                myPlotter.firstHorizontal,
            )

            mySensor.DrawSensor(
                myPlotter.draw,
                myPlotter.fonts,
                0,
                0,
                myPlotter.secondVertical - 100,
                myPlotter.firstHorizontal,
            )
            #myPlotter.ShowImage()

            if myPlotter.EpdInit() == True:
                myPlotter.Display()

except KeyboardInterrupt:
    myPlotter.EpdSleep()
    if mySensor.connected:
        mySensor.Disconnect()
