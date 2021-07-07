import asyncio
import websockets
import time
import json
from bson import json_util
from DAL.Tick import Tick

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
    print('1')
    start_server = websockets.serve(binance_stream_server, "192.168.224.3", 3549)


    print('2')
    asyncio.get_event_loop().run_until_complete(start_server)


    print('3')
    asyncio.get_event_loop().run_forever()


    print('4')
except Exception as e:
    print('ERROR: ')
    print(e)