import os
import sys

libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "lywsd03mmc")
if os.path.exists(libdir):
    sys.path.append(libdir)

from lywsd03mmc_client import Lywsd03mmcClient,Lywsd03mmcClientSyncContext, Lywsd03mmcData
import asyncio

MAC_ADDRESS_OR_UUID = 'A4:C1:38:1C:F3:96'


async def main(address):
    async with Lywsd03mmcClient(address, timeout=60) as client:
        lywsd03mmc_data = await client.get_data()
        print(lywsd03mmc_data)


asyncio.run(main(MAC_ADDRESS_OR_UUID))
