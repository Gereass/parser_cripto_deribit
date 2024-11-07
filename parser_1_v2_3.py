# откр бд отк кон
import asyncio
import json
import aiohttp
import sqlite3
import time

MAIN_COUNTER = list()


#функция для парсинга данных и внесения данных в бд
async def call_api(ws, conn):
    #создание бд если она не была создана ранее
    cursor = conn.cursor()
    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS my_table (
    #     timestamp TEXT,
    #     index_price REAL NOT NULL,
    #     instrument_name TEXT NOT NULL)
    # ''')
    # conn.commit()
    # conn.close()

    name_val = ['BTC','ETH']
    ticker_name = list()

    data_result = dict()
    sorted_data = dict()
    
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

        cursor.execute('''
            INSERT INTO my_table(timestamp,index_price,instrument_name)
            VALUES(?,?,?)
        ''', (sorted_data['timestamp'],sorted_data['index_price'],sorted_data['instrument_name']))
        conn.commit()

# Откр бд, отк вб
async def main():
    conn = sqlite3.connect('data_pars.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS my_table (
        timestamp TEXT,
        index_price REAL NOT NULL,
        instrument_name TEXT NOT NULL)
    ''')
    conn.commit()
    conn.close()


    time_s = 0 
    conn = sqlite3.connect('data_pars.db')
    #вызов функций для запроса данных
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('wss://test.deribit.com/ws/api/v2') as ws:     
            for i in (range(30)):
                start_t = time.perf_counter()

                await call_api(ws, conn)
                await asyncio.sleep(40)
                end_t = time.perf_counter()
                time_s = end_t - start_t
                MAIN_COUNTER.append(time_s)
                print(time_s)


    conn.close()


        
        # while True:
        #     await call_api(session)

time_start_all = time.perf_counter()
# for i in range(0,30):
asyncio.get_event_loop().run_until_complete(main())
time_end_all = time.perf_counter()

time_s_all = time_end_all - time_start_all

print(MAIN_COUNTER, '03 интервал 40 сек, общее время: ', time_s_all)