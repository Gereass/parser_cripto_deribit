import asyncio
import json
import aiohttp
import sqlite3


#функция для парсинга данных и внесения данных в бд
async def call_api(session, msg):
    async with session.ws_connect('wss://test.deribit.com/ws/api/v2') as ws:
        await ws.send_json(msg)

        data_result = dict()
        sorted_data = dict()

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
        

async def main():
    #переменные для отправки json запроса на сервис
    msg_BTC = \
    {
      "jsonrpc" : "2.0",
      "id" : 8106,
      "method" : "public/ticker",
      "params" : {
        "instrument_name" : "BTC-PERPETUAL"
      }
    }
    msg_ETH = \
    {
      "jsonrpc" : "2.0",
      "id" : 8106,
      "method" : "public/ticker",
      "params" : {
        "instrument_name" : "ETH-PERPETUAL"
      }
    }

    #создание бд если она не была создана ранее
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

    #вызов функций для запроса данных
    async with aiohttp.ClientSession() as session:
      while True:
        await call_api(session, msg_BTC)
        await call_api(session, msg_ETH)
        await asyncio.sleep(60)


asyncio.get_event_loop().run_until_complete(main())