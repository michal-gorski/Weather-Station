import os
import sys

libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "lywsd03mmc")
if os.path.exists(libdir):
    sys.path.append(libdir)

from lywsd03mmc_client import Lywsd03mmcClientSyncContext, Lywsd03mmcData

MAC_ADDRESS_OR_UUID = 'A4:C1:38:1C:F3:96'

while True:
    try:
        with Lywsd03mmcClientSyncContext(MAC_ADDRESS_OR_UUID, timeout_sec=30) as client:
            data: Lywsd03mmcData = client.get_data()
            print(data)
    except Exception as ex:
        print(f"Error: {ex}")
