import plotter
import clock
import schoolPlan
import weatherWarnings
import smog
import forecast
import datetime
import sensor
import asyncio
import signal
import logging

logger = logging.getLogger(__name__)

class WeatherStation:
    
    forecast = None
    
    def __init__(self) -> None:
        # Event used to trigger graceful shutdown from signal handlers
        self._shutdown = asyncio.Event()

    async def RunWeatherStation(self):        
        self.sensor = sensor.Sensor()

        await self.sensor.Connect()

        self.plotter = plotter.Plotter(800, 480)
        self.plotter.EpdInit()

        # Register signal handlers so Ctrl-C / SIGTERM trigger shutdown
        loop = asyncio.get_running_loop()
        try:
            loop.add_signal_handler(signal.SIGINT, self._shutdown.set)
            loop.add_signal_handler(signal.SIGTERM, self._shutdown.set)
        except NotImplementedError:
            # add_signal_handler may not be implemented on some platforms
            logger.debug("Signal handlers not registered (platform limitation)")

        try:
            # Run an initial update immediately
            await self._update_and_draw()

            # Loop, sleeping until the start of the next minute to avoid busy-waiting
            while not self._shutdown.is_set():
                now = datetime.datetime.now()
                # seconds until the next minute boundary
                seconds_to_next = 60 - now.second - now.microsecond / 1_000_000

                # Wait for either the shutdown event or the timeout to expire
                try:
                    await asyncio.wait_for(self._shutdown.wait(), timeout=seconds_to_next)
                except asyncio.TimeoutError:
                    # timeout expired -> time to run the next update
                    pass

                if self._shutdown.is_set():
                    break

                await self._update_and_draw()
        finally:
            await self._cleanup()

    async def _update_and_draw(self):
        """Perform a single data fetch + draw cycle."""
        # Determine current minute
        current_minute = datetime.datetime.now().minute

        # Get data every 10 minutes or on first run
        if self.forecast is None or current_minute % 10 == 0:
            self.forecast = forecast.Forecast()
            self.smog = smog.Smog()
            self.warnings = weatherWarnings.WeatherWarnings()
            self.plan = schoolPlan.SchoolPlan()
            self.plan.CurrentPlan()

        self.clock = clock.Clock()

        # sensor data
        if self.sensor.connected:
            await self.sensor.GetData()

        # draw data
        logger.info("Starting redraw")
        self.plotter.PrepareGrid()

        self.plan.DrawPlan(
            self.plotter.draw,
            self.plotter.fonts,
            0,
            self.plotter.firstHorizontal,
            self.plotter.firstVertical,
            self.plotter.height,
        )
        self.clock.DrawClock(
            self.plotter.draw,
            self.plotter.fonts,
            self.plotter.secondVertical,
            0,
            self.plotter.width,
            self.plotter.firstHorizontal,
        )
        self.forecast.DrawForecast(
            self.plotter.draw,
            self.plotter.fonts,
            self.plotter.icons,
            self.plotter.firstVertical,
            self.plotter.fourthHorizontal,
            self.plotter.width - 12,
            self.plotter.height,
        )
        self.forecast.DrawHourly(
            self.plotter.draw,
            self.plotter.fonts,
            self.plotter.icons,
            self.plotter.firstVertical,
            self.plotter.firstHorizontal,
            self.plotter.width - 12,
            self.plotter.thirdHorizontal,
        )
        self.warnings.DrawWarnings(
            self.plotter.draw,
            self.plotter.fonts,
            self.plotter.firstVertical,
            self.plotter.thirdHorizontal,
            self.plotter.width,
            self.plotter.fourthHorizontal,
        )
        self.smog.DrawSmog(
            self.plotter.draw,
            self.plotter.fonts,
            self.plotter.secondVertical - 100,
            0,
            self.plotter.secondVertical,
            self.plotter.firstHorizontal,
        )

        self.sensor.DrawSensor(
            self.plotter.draw,
            self.plotter.fonts,
            0,
            0,
            self.plotter.secondVertical - 100,
            self.plotter.firstHorizontal,
        )

        if self.plotter.epdReady:
            self.plotter.Display()
        else:
            self.plotter.ShowImage()

    async def _cleanup(self):
        """Clean up hardware and connections on shutdown.

        This method is resilient: it logs and continues on individual errors so
        that the best-effort shutdown sequence completes.
        """
        logger.info("Shutting down: cleaning up resources")
        try:
            if hasattr(self, 'plotter') and self.plotter:
                try:
                    # put the display into low-power mode if supported
                    self.plotter.EpdSleep()
                except Exception:
                    logger.exception("Error putting EPD to sleep")

            if hasattr(self, 'sensor') and self.sensor:
                try:
                    res = self.sensor.Disconnect()
                    if asyncio.iscoroutine(res):
                        await res
                except Exception:
                    logger.exception("Error disconnecting sensor")
        except Exception:
            logger.exception("Unexpected error during cleanup")
            
if __name__ == "__main__":
    # configure logging first, then set module logger level
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("weatherstation.log"),
            logging.StreamHandler()
        ]
    )
    logger.setLevel(logging.INFO)


    try:
        weatherStation = WeatherStation()
        asyncio.run(weatherStation.RunWeatherStation())
    
    except KeyboardInterrupt:
        if hasattr(weatherStation, 'plotter') and weatherStation.plotter:
            weatherStation.plotter.EpdSleep()
        if hasattr(weatherStation, 'sensor') and weatherStation.sensor and weatherStation.sensor.connected:
            weatherStation.sensor.Disconnect()