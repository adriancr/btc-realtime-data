import asyncio
import websockets
import time
import json
from bson import json_util
from DAL.Tick import Tick

import socket


ip = False
port = 3549

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

async def binance_stream_server(websocket, path):
    tick = Tick()
    
    while True:
        data = tick.getLatest()
        event = False

        for document in data:
          event = document

        # data = json_util.dumps(data)
        # print(data)
        new_data = {
            "price": data['close'],
            "change": data['velocity']
        }

        print(new_data)
        await websocket.send(json_util.dumps(new_data))
        time.sleep(1)
    
    # name = await websocket.recv()
    # print(f"< {name}")

    # greeting = f"Hello {name}!"

    # await websocket.send(greeting)
    # print(f"> {greeting}")

try:
    ip = get_ip()
    print(f'Beginning stream at ws://{ip}:{port}')
    start_server = websockets.serve(binance_stream_server, ip, port)
    asyncio.get_event_loop().run_until_complete(start_server)
    
    print('Connection completed, stream running')
    asyncio.get_event_loop().run_forever()


    print('4')
except Exception as e:
    print('ERROR: ')
    print(e)