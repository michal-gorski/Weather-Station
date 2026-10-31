from PIL import Image, ImageDraw, ImageFont
import imageHelper
import logging
logger = logging.getLogger(__name__)

import asyncio
from bleak import BleakScanner, BleakClient

import sys


class Sensor:
    TEMP_ID = "00002a1f-0000-1000-8000-00805f9b34fb"
    HUMIDITY_ID = "00002a6f-0000-1000-8000-00805f9b34fb"

    # None until a reading succeeds, so the display shows "--" instead of a fake 0
    temperature = None
    humidity = None
    sensorName = "Taras"
    client = ""
    device = ""
    connected = False

    def __init__(self) -> None:
        pass

    def PrintSensor(self):
        print(
            "Sensor: " + self.sensorName,
            "| Temperature: ",
            self.temperature,
            " | Humidity: ",
            self.humidity,
        )

    def DrawSensor(
        self, draw: ImageDraw.ImageDraw, fonts, x1: int, y1: int, x2: int, y2: int
    ):
        temperature = "--" if self.temperature is None else str(self.temperature)
        humidity = "--" if self.humidity is None else str(round(self.humidity))
        draw.text((x1 + 15, y1 + 5), "TARAS", 0, fonts["font18"])
        draw.text(
            (x1 + 15, y1 + 18),
            temperature + "°",
            font=fonts["font48bold"],
            fill=0,
        )
        draw.text(
            (x1 + 15, y1 + 65),
            humidity + "%",
            font=fonts["font30bold"],
            fill=0,
        )
        imageHelper.DrawDottedVerticalLine(draw, 145, 0, y2, 4)

        draw.text((x1 + 155, y1 + 5), "SALON", 0, fonts["font18"])
        draw.text((x1 + 155, y1 + 18), "--°", font=fonts["font48bold"], fill=0)
        draw.text((x1 + 155, y1 + 65), "--%", font=fonts["font30bold"], fill=0)
        imageHelper.DrawDottedVerticalLine(draw, 285, 0, y2, 4)

    async def Connect(self) -> bool:
        logger.info("Starting Sensor connection")
        try:
            # drop a stale connection left over from a failed read
            await self.Disconnect()
            devices = await BleakScanner.discover(timeout=10)
            for d in devices:
                logger.debug("Found device: " + str(d))
                
                if d.name != None and d.name.startswith("ATC"):
                    self.device = d
                    logger.info("Connecting to: " + str(d))
                    client = BleakClient(d, timeout=30)

                    await client.connect()
                    logger.info("Connected to: " + str(d))

                    #for service in client.services:
                    #    for char in service.characteristics:
                    #        print(char)

                    self.client = client
                    self.connected = True
                    await self.GetData()
                    return self.connected
            logger.warning("Sensor not found among " + str(len(devices)) + " devices")
        except Exception as e:
            logger.error(str(e))
        self.client = ""
        self.connected = False
        self.temperature = None
        self.humidity = None
        return False

    async def GetData(self):
        try:
            logger.info('getting data from sensor:' + str(self.device))
            temp_bytes = await self.client.read_gatt_char(self.TEMP_ID)
            self.temperature = (
                int.from_bytes(temp_bytes[:2], byteorder="little", signed=True) / 10
            )

            hum_bytes = await self.client.read_gatt_char(self.HUMIDITY_ID)
            self.humidity = (
                int.from_bytes(hum_bytes[:2], byteorder="little", signed=True) / 100
            )

            logger.info("temp:" + str(self.temperature) + " hum: " + str(self.humidity))
        except Exception as e:
            logger.error("Sensor read failed: " + str(e))
            self.connected = False

    async def Disconnect(self):
        if not self.client:
            return
        logger.info("Disconnecting from " + str(self.device))
        try:
            await self.client.disconnect()
        finally:
            self.client = ""
            self.connected = False
