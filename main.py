import logging
logger = logging.getLogger(__name__)

logging.basicConfig(filename='myapp.log', level = logging.INFO)
logger.info('Initializing...')

logger.info('Getting forecast')
import forecast
#myForecast = forecast.Forecast()
#myForecast.PrintForecast()

logger.info('Getting Smog Data')
import smog
#mySmog = smog.Smog()
#mySmog.PrintSmog()

logger.info('Getting Warnings Data')
import weatherWarnings
#myWarnings = weatherWarnings.WeatherWarnings()
#myWarnings.PrintWarnings()

logger.info('Getting school plan')
import schoolPlan
myPlan = schoolPlan.SchoolPlan()
myPlan.CurrentPlan()
myPlan.PrintPlan()

logger.info('Initializing plotter')
import plotter
myPlotter = plotter.Plotter(1600,960)
myPlotter.PrepareGrid()

myPlan.DrawPlan(myPlotter.draw,0,myPlotter.firstHorizontal,myPlotter.firstVertical,myPlotter.height)


myPlotter.ShowImage()