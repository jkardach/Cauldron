import asyncio
from bleak import BleakClient


LED_UUID = "c8c9b555-53a3-46f6-97d0-4e642b6d4526"

RED_HEX = b"\xff\xff\x00\xff"


async def main():
    async with BleakClient("FD:6E:13:0F:51:C5", timeout=30) as client:
        await client.write_gatt_char(LED_UUID, RED_HEX, response=False)


# Using asyncio.run() is important to ensure that device disconnects on
# KeyboardInterrupt or other unhandled exception.
asyncio.run(main())
