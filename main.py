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
import logging.handlers
import os
import time

logger = logging.getLogger(__name__)

class WeatherStation:

    # How often online data is fetched and a lost sensor reconnected
    DATA_REFRESH_SECONDS = 10 * 60

    forecast = None

    def __init__(self) -> None:
        # Event used to trigger graceful shutdown from signal handlers
        self._shutdown = asyncio.Event()
        self._lastRefresh = None

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
            await self._safe_update_and_draw()

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

                await self._safe_update_and_draw()
        finally:
            await self._cleanup()

    async def _safe_update_and_draw(self):
        """Run one cycle; a failure is logged and retried next minute instead of stopping the station."""
        try:
            await self._update_and_draw()
        except Exception:
            logger.exception("Update cycle failed")

    async def _refresh_data(self):
        """Fetch online data and reconnect the sensor if it was lost."""
        newForecast = forecast.Forecast()
        # keep showing the previous forecast if this fetch failed
        if self.forecast is None or newForecast.forecast:
            self.forecast = newForecast
        self.smog = smog.Smog()
        self.warnings = weatherWarnings.WeatherWarnings()
        self.plan = schoolPlan.SchoolPlan()

        if not self.sensor.connected:
            await self.sensor.Connect()

        self._lastRefresh = time.monotonic()

    async def _update_and_draw(self):
        """Perform a single data fetch + draw cycle."""
        if self._lastRefresh is None or time.monotonic() - self._lastRefresh >= self.DATA_REFRESH_SECONDS:
            await self._refresh_data()

        # the plan switches to the next day in the afternoon, so pick the day every cycle
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
    logPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "weatherstation.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            # the station logs every minute, so cap the file at 3 x 1 MB
            logging.handlers.RotatingFileHandler(logPath, maxBytes=1_000_000, backupCount=2),
            logging.StreamHandler()
        ]
    )
    logger.setLevel(logging.INFO)


    try:
        weatherStation = WeatherStation()
        asyncio.run(weatherStation.RunWeatherStation())

    except KeyboardInterrupt:
        # Ctrl-C during the initial BLE scan, before signal handlers are
        # registered; the display isn't initialised yet so there is nothing to clean up
        logger.info("Interrupted")
