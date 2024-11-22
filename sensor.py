from PIL import Image, ImageDraw, ImageFont
import imageHelper

import asyncio
from bleak import BleakScanner, BleakClient

import sys


class Sensor:
    TEMP_ID = "00002a1f-0000-1000-8000-00805f9b34fb"
    HUMIDITY_ID = "00002a6f-0000-1000-8000-00805f9b34fb"

    temperature = 24.1
    humidity = 38
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
        draw.text((x1 + 10, y1 + 5), "TARAS", 0, fonts["font18"])
        draw.text(
            (x1 + 10, y1 + 18),
            str(self.temperature) + "°",
            font=fonts["font48bold"],
            fill=0,
        )
        draw.text(
            (x1 + 10, y1 + 65),
            str(self.humidity) + "%",
            font=fonts["font30bold"],
            fill=0,
        )
        imageHelper.DrawDottedVerticalLine(draw, 140, 0, y2, 4)

        draw.text((x1 + 150, y1 + 5), "SALON", 0, fonts["font18"])
        draw.text((x1 + 150, y1 + 18), "--°", font=fonts["font48bold"], fill=0)
        draw.text((x1 + 150, y1 + 65), "--%", font=fonts["font30bold"], fill=0)
        imageHelper.DrawDottedVerticalLine(draw, 280, 0, y2, 4)

    async def Connect(self) -> bool:
        try:
            devices = await BleakScanner.discover(timeout=10)
            for d in devices:
                print(d)
                print(d.name)
                self.device = d
                if d.name.startswith("ATC"):
                    print("Connecting to", d)
                    client = BleakClient(d, timeout=30)

                    await client.connect()
                    print("connected!")

                    for service in client.services:
                        for char in service.characteristics:
                            print(char)

                    self.client = client
                    self.connected = True
                    return True
        except Exception as e:
            print(str(e))
            self.client = ""
            self.connected = False
            return False

    async def GetData(self):
        try:
            print('getting data from sensor:',str(self.device))
            temp_bytes = await self.client.read_gatt_char(self.TEMP_ID)
            self.temperature = (
                int.from_bytes(temp_bytes[:2], byteorder="little", signed=True) / 10
            )

            hum_bytes = await self.client.read_gatt_char(self.HUMIDITY_ID)
            self.humidity = (
                int.from_bytes(hum_bytes[:2], byteorder="little", signed=True) / 100
            )

            print("temp:", self.temperature, " hum: ", self.humidity)
        except Exception as e:
            self.connected = False
            print(str(e))

    async def Disconnect(self):
        print("Disconnecting from", self.device)
        await self.client.disconnect()
