import asyncio
import bleak

async def main():
    devices = await bleak.BleakScanner.discover(8)
    for device in devices:
        print(f"{device.name} ({device.address})")

# Run the main function
#asyncio.run(main())

address = "A4:C1:38:1C:F3:96"
TEMP_ID = "00002a1f-0000-1000-8000-00805f9b34fb"

async def readData(address):
    async with bleak.BleakClient(address) as client:
        if (not client.is_connected):
            raise "client not connected"
        services = await client.get_services()

        temp_bytes = await client.read_gatt_char(TEMP_ID)
        print('temp',temp_bytes)    

asyncio.run(readData(address))

