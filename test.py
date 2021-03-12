import asyncio
from encryption import Encryption
from xmpp import XMPPConnector
import os
from dotenv import load_dotenv


load_dotenv()

MAGIC_NEFIT = bytearray.fromhex(
    "58f18d70f667c9c79ef7de435bf0f9b1553bbb6e61816212ab80e5b0d351fbb1"
)

MAGIC_IVT = bytearray.fromhex(
    "867845e97c4e29dce522b9a7d3a3e07b152bffadddbed7f5ffd842e9895ad1e4"
)

HOST = os.getenv('HOST')
ACCESS_KEY = os.getenv('ACCESS_KEY')
PASSWORD = os.getenv('PASSWORD')
TO_DECRYPT = os.getenv('TO_DECRYPT')

async def main():
    loop = asyncio.get_event_loop()
    
    encryption = Encryption(access_key=ACCESS_KEY, password=PASSWORD, magic=MAGIC_NEFIT)
    connector = XMPPConnector(
        host=HOST,
        loop=loop,
        access_key=ACCESS_KEY,
        encryption=encryption,
    )
    print(await connector.get("/gateway/uuid"))

def just_decrypt():
    print("SUCCESS IF MSG LOOK LIKE READABLE JSON")
    print("MAGIC IVT")
    print("")
    enc1 = Encryption(access_key=ACCESS_KEY, password=PASSWORD, magic=MAGIC_IVT)
    enc1.decrypt(enc=TO_DECRYPT)
    
    print("")
    print("MAGIC NEFIT")
    print("")

    enc2 = Encryption(access_key=ACCESS_KEY, password=PASSWORD, magic=MAGIC_NEFIT)
    enc2.decrypt(enc=TO_DECRYPT)

    print("")
    print("MAGIC UNKNOWN")
    print("")

    magic = bytearray()
    magic.extend("qNuxaCVIT1N3TCUhnMGd".encode())
    enc3 = Encryption(access_key=ACCESS_KEY, password=PASSWORD, magic=magic)
    enc3.decrypt(enc=TO_DECRYPT)

if TO_DECRYPT:
    just_decrypt()
else:
    print("Nothing to decrypt, sending GET")
    asyncio.get_event_loop().run_until_complete(main())
