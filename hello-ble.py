import asyncio
from bleak import BleakScanner, BleakClient

import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# note:
#   The default configuration of the devices is not connectable by the bluetooth HCI interface in linux.
#   Use a tool such as https://gist.github.com/mironovdm/cb7f47e8d898e9a3977fc888d990e8a9 to increase the
#       default HCI timeout and the devices will be connectable.


async def main():
    devices = await BleakScanner.discover(timeout=10)
    for d in devices:
        print(d)
        print(d.rssi)
        if d.name.startswith("ATC_1CF396"):
            print("Connecting to", d)
            client = BleakClient(d, timeout=30)
            try:
                await client.connect()
                print("connected!")

                for service in client.services:
                    for char in service.characteristics:
                        print(char)
            finally:
                print("Disconnecting from", d)
                await client.disconnect()

            break

asyncio.run(main())