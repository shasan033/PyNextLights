import asyncio
from bleak import BleakClient
import logging
import sys

MAIN_CHARACTERISTIC_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
MAIN_MAC_ADDRESS = "30:58:89:42:96:6A"


async def write_characteristic(device, uuid, value):
    try:
        await device.write_gatt_char(uuid, bytearray(value))
    except Exception as e:
        raise Exception(f"Error writing characteristic: {str(e)}")

    logging.info(f"Characteristic written: {value} => {uuid}")


async def turn_on(device):
    await write_characteristic(device, MAIN_CHARACTERISTIC_UUID, b'\x55\x01\x02\x01')
    logging.info("Device turned on")


async def turn_off(device):
    await write_characteristic(device, MAIN_CHARACTERISTIC_UUID, b'\x55\x01\x02\x00')
    logging.info("Device turned off")


async def set_rgb(r: int, g: int, b: int, device):
    payload = [85, 7, 1, r, g, b]

    await write_characteristic(device, MAIN_CHARACTERISTIC_UUID, bytearray(payload))
    logging.info(f"Set RGB to [{r}, {g}, {b}]")


async def main(mac):
    async with BleakClient(mac) as client:
        try:
            await turn_on(client)
            await asyncio.sleep(5)
            await turn_off(client)
        except Exception as e:
            logging.error(f"Error resulted in running script: {str(e)}")


if __name__ == '__main__':
    command = sys.argv[1]
    asyncio.run(main(MAIN_MAC_ADDRESS))