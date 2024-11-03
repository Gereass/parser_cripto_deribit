import asyncio
import json
import aiohttp
import sqlite3


name_val = ['BTC','ETH']
conn = sqlite3.connect('data_pars.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS my_table (
    timestamp TEXT,
    index_price REAL NOT NULL,
    instrument_name TEXT NOT NULL
)
''')
conn.commit()
conn.close()


data_result = dict()
sorted_data = dict()

name_val = ['BTC','ETH']
ticker_name = list()


async def take_all_ticker_name(session):
    async with session.ws_connect('wss://test.deribit.com/ws/api/v2') as ws:
        for i in name_val:
            msg = \
                {
                "jsonrpc" : "2.0",
                "id" : 9344,
                "method" : "public/get_book_summary_by_currency",
                "params" : {
                    "currency" : i,
                    "kind" : "future"
                }
                }
            await ws.send_json(msg)
            response = await ws.receive()
            data = json.loads(response.data)

            for i in range(len(data['result'])):
                ticker_name.append(data['result'][i]['instrument_name'])

     
async def call_api(session):
    async with session.ws_connect('wss://test.deribit.com/ws/api/v2') as ws:
        for i in ticker_name:
            msg = \
                {
                "jsonrpc" : "2.0",
                "id" : 8106,
                "method" : "public/ticker",
                "params" : {
                    "instrument_name" : i
                }
                }
            
            await ws.send_json(msg)

            response = await ws.receive()
            data = json.loads(response.data)
            data_result = data['result']
            
            sorted_data = { 
                "timestamp":data_result['timestamp'],
                "index_price":data_result['index_price'],
                "instrument_name":data_result['instrument_name'],
                }
            
            conn = sqlite3.connect('data_pars.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO my_table(timestamp,index_price,instrument_name)
                VALUES(?,?,?)
            ''', (sorted_data['timestamp'],sorted_data['index_price'],sorted_data['instrument_name']))
            conn.commit()
            conn.close()
            
            print(sorted_data)
            

async def main():
        async with aiohttp.ClientSession() as session:
            await take_all_ticker_name(session)
            while True:
                await call_api(session)
                await asyncio.sleep(20)




asyncio.get_event_loop().run_until_complete(main())