# from pymongo import MongoClient
import pymongo
import os

class Tick:

    DB_HOST = os.environ['MONGODB_HOSTNAME']
    DB_USER = os.environ['MONGODB_USERNAME']
    DB_PSW = os.environ['MONGODB_PASSWORD']
    DB_PORT = 27017
    DB_NAME = os.environ['MONGODB_DATABASE']

    DB_COLLECTION_NAME = 'Ticks'
    DB_COLS = { 
        'open': "float", 
        'close': "float", 
        'high': "float", 
        'low': "float", 
        'volume': "float", 
        'ts': "timestamp", 
        'trades_count': "float", 
        'asset_volume': "float", 
        'quote_asset_volume': "float", 
        'tb_base_asset_volumne': "float", 
        'tb_quote_asset_volume': "float"
    }

    MongoDBClient = False
    DBConn = False
    db = False
    dbData = False

    previousClose = 0


    def __init__(self):

        # print(self.DB_HOST, self.DB_USER, self.DB_PSW, self.DB_PORT, self.DB_NAME)
        
        # Start Mongo client
        self.MongoDBClient = pymongo.MongoClient(self.DB_HOST, self.DB_PORT)

        # Connect to DB
        self.DBConn = self.MongoDBClient[self.DB_NAME]
        
        # Authenticate to DB
        self.DBConn.authenticate(self.DB_USER, self.DB_PSW)

        # Get collection (table) specific DB access object
        self.db = self.DBConn.Ticks

        print(self.DBConn, self.db)


    def initialize(self, item):
        self.dbData = {}
        for key in self.DB_COLS:
            if key in item:
                dataType = self.DB_COLS[key]

                if(dataType == 'float'):
                    self.dbData[key] = float(item[key])
                    pass

                elif(dataType == 'timestamp'):
                    self.dbData[key] = item[key]
                    pass


    def setPreviousClose(self, closePrice):
        self.previousClose = float(closePrice)

        

    def preliminaryCalculations(self):
        # High - Low Amount
        self.dbData['hl_difference'] = self.dbData['high'] - self.dbData['low']

        # High - Low Percentage
        self.dbData['hl_difference_percentage'] = self.dbData['hl_difference'] * 100 / self.dbData['high']

        # Open - Close Amount
        self.dbData['oc_difference'] = self.dbData['open'] - self.dbData['close']
        
        # Open - Close Amount Percentage
        self.dbData['oc_difference_percentage'] = self.dbData['oc_difference'] * 100 / self.dbData['open']

        # Average open / close
        self.dbData['oc_average'] = (self.dbData['open'] + self.dbData['close']) / 2

    def extraCalcs(self):
        # Velocity
        if self.previousClose > 0:
            self.dbData['velocity'] = self.previousClose - self.dbData['close']
            print(f'V: ${self.dbData["velocity"]}')


    def save(self):
        # print(self.dbData)
        self.db.insert(self.dbData)