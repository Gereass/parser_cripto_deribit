from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.params import Query
from typing import List
import sqlite3
import json

app = FastAPI()

# Подключение к базе данных
conn = sqlite3.connect('data_pars.db')
cursor = conn.cursor()

# Получение всех сохраненных данных по указанной валюте
@app.get("/get_all_data/")
async def get_all_data(ticker: str = Query(..., description="Тикер валюты")):
    cursor.execute("SELECT * FROM my_table WHERE instrument_name =?", (ticker,))
    data = cursor.fetchall()
    if not data:
        raise HTTPException(status_code=404, detail="Данные не найдены")
    return JSONResponse(content=data, media_type="application/json")

# Получение последней цены валюты
@app.get("/get_last_price/")
async def get_last_price(ticker: str = Query(..., description="Тикер валюты")):
    cursor.execute("SELECT index_price FROM my_table WHERE instrument_name =? ORDER BY timestamp DESC LIMIT 1", (ticker,))
    data = cursor.fetchone()
    if not data:
        raise HTTPException(status_code=404, detail="Данные не найдены")
    return JSONResponse(content={"index_price": data[0]}, media_type="application/json")

# Получение цены валюты с фильтром по дате, дата должна быть в формате unix
@app.get("/get_price_by_date/")
async def get_price_by_date(ticker: str = Query(..., description="Тикер валюты"), date: str = Query(..., description="Дата в формате YYYY-MM-DD")):
    cursor.execute("SELECT index_price FROM my_table WHERE instrument_name =? AND timestamp =?", (ticker, date))
    data = cursor.fetchone()
    if not data:
        raise HTTPException(status_code=404, detail="Данные не найдены")
    return JSONResponse(content={"price": data[0]}, media_type="application/json")
