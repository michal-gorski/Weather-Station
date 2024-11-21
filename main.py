import logging
logger = logging.getLogger(__name__)

logging.basicConfig(filename='myapp.log', level = logging.INFO)
logger.info('Initializing...')

logger.info('Getting forecast')
import forecast
myForecast = forecast.Forecast()
myForecast.PrintForecast()

logger.info('Getting Smog Data')
import smog
mySmog = smog.Smog()
mySmog.PrintSmog()

logger.info('Getting Warnings Data')
import weatherWarnings
myWarnings = weatherWarnings.WeatherWarnings()
myWarnings.PrintWarnings()

logger.info('Getting school plan')
import schoolPlan
myPlan = schoolPlan.SchoolPlan()
myPlan.CurrentPlan()
myPlan.PrintPlan()

logger.info('Getting clock')
import clock
myClock = clock.Clock()
myClock.PrintClock()

logger.info('Initializing plotter')
import plotter
myPlotter = plotter.Plotter(800,480)
myPlotter.PrepareGrid()

myPlan.DrawPlan(myPlotter.draw,myPlotter.fonts,0,myPlotter.firstHorizontal,myPlotter.firstVertical,myPlotter.height)
myClock.DrawClock(myPlotter.draw,myPlotter.fonts,myPlotter.secondVertical,0,myPlotter.width,myPlotter.firstHorizontal)
myForecast.DrawForecast(myPlotter.draw,myPlotter.fonts,myPlotter.firstVertical,myPlotter.firstHorizontal,myPlotter.width,myPlotter.secondHorizontal)

myPlotter.ShowImage()