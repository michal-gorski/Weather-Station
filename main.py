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

logger.info('Initializing plotter')
import plotter
myPlotter = plotter.Plotter()
