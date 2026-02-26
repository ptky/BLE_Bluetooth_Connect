#file transfer via bluetooth

# must install bleak (pip install bleak) before running

import asyncio, bleak
from bleak import BleakScanner,BleakClient

def get_info(size:int):
     qstn = int(input("Enter the number of the device you want to connect to: "))
     while qstn > size or qstn < 1:
          qstn = int(input("Wrong number! Enter the number of device you want to connect to: "))
     return qstn


async def search_devices():
     devices = await BleakScanner.discover(5)
     size = len(devices)
     for i in range(size):
          print(f"[{i+1}.] device: {devices[i]}")
     data = get_info(size=size)
     return devices[data-1]
      
async def connect():
     choosen_device =  await search_devices()
     address = choosen_device.address
     print(f"Successfully choosen: {choosen_device.name}")
     print(f"\nTrying to connect to {address}")
     device = await BleakScanner.find_device_by_address(address,timeout=10)
     if(device == None):
          print("failuire")
     else:
          print("client found, connecting")
          async with BleakClient(device) as c:
               print(f"Client connection: = {c.is_connected}")     
          print("\ndisconnected")

if __name__ == "__main__":
     asyncio.run(connect())