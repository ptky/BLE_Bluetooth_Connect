#file transfer via bluetooth

# must install bleak (pip install bleak) before running

import asyncio, bleak
from bleak import BleakScanner,BleakClient


# ez mindenkinek a sajatja ahonnan hostolja es akar uzenetet kuldeni 
service_uuid = "12345678-1234-5678-1234-56789abcdef0"
char_uuid = "abcdef01-2345-6789-abcd-ef0123456789"
hard_coded_message = "Pumbu, horcsog"

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

def notification_handler(sender, data):
    print(f"Notification from {sender}: {data.decode()}")

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
               await c.start_notify(char_uuid, notification_handler)
               qstn1 = input("send a message? Y/N: ")
               if qstn1 == "y" or qstn1 == "Y":
                    await c.write_gatt_char(char_uuid, hard_coded_message.encode())
                    print("message sent (we hope)")


               await asyncio.sleep(30)     
          print("\ndisconnected")

if __name__ == "__main__":
     asyncio.run(connect())