import time, resource
import websocket, json
from datetime import datetime
from DAL.Tick import Tick

class Stream:
    
    MAIN_URL = 'wss://stream.binance.com:9443'

    Symbol = ''
    Interval = ''
    SocketUrl = ''

    ws = False
    # db = False
    previousMessage = False

    def __init__(self, symbol, interval):
        self.Symbol = symbol
        self.Interval = interval
        self.SocketUrl = f'{self.MAIN_URL}/ws/{self.Symbol}@kline_{self.Interval}'

        print("Beginning connection for Stream " + self.SocketUrl)
        self.ws = websocket.WebSocketApp(self.SocketUrl, 
                    # on_open = lambda ws: self.on_open(ws),
                    on_message = lambda ws, message: self.on_message(ws, message), 
                    on_close = lambda ws, close_status_code, close_msg: self.on_close(ws, close_status_code, close_msg)) 
                    # on_open = self.on_open

        self.tick = Tick()


    def start(self):
        print("Openning stream")
        self.ws.run_forever()


    def on_message(self, ws, message):
        
        try:
            # Performance metrics: time
            time_start = time.perf_counter()

            # Load stream data as json
            msgData = json.loads(message)
            
            # Python timestamp is based on seconds, Binance timestamp is based on milliseconds
            # Divide by 1000: https://stackoverflow.com/questions/748491/how-do-i-create-a-datetime-in-python-from-milliseconds
            ts = datetime.fromtimestamp(msgData['E'] / 1000).isoformat()

            # Map data to create new Tick object
            tickData = {
                'ts': ts,
                'open': msgData['k']['o'],
                'close': msgData['k']['c'],
                'high': msgData['k']['h'],
                'low': msgData['k']['l'],
                'volume': msgData['k']['v'],
                'trades_count': msgData['k']['n'],
                'quote_asset_volume': msgData['k']['q'],
                'tb_base_asset_volumne': msgData['k']['V'],
                'tb_quote_asset_volume': msgData['k']['Q'],
                'minute_closed': msgData['k']['x']
            }

            # Initialize Tick object with data received
            self.tick.initialize(tickData)

            # Set previous close, used to implement additional calculations
            if self.previousMessage:
                self.tick.setPreviousClose(self.previousMessage['k']['c'])
            
            # Make some basic calculations
            self.tick.preliminaryCalculations()
            
            # Make additional calculations
            self.tick.extraCalcs()

            # Save data into DB
            self.tick.save()

            # Set previousMessage so we can calculate additional data
            self.previousMessage = msgData
            
            # Performance metrics: time and mem
            time_elapsed = round(time.perf_counter() - time_start, 5)
            memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0/1024.0
            print(f'{ts}: ${round(float(msgData["k"]["c"]), 2)}. PERF: t: {time_elapsed}; m: {memory}')

        except Exception as e:
            print('on_message ERROR: ')
            print(e)



    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")

