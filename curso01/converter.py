import requests
from os import getenv
import aiohttp
from fastapi import HTTPException

APIKEY = getenv('APIKEY')

def sync_converter(from_currency: str, to_currencies: str, price: float):
    url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currencies}&apikey={APIKEY}'

    try:
        response = requests.get(url)
    except Exception as error:
        raise HTTPException(status_code=400, detail=error)
    
    
    data = response.json()
    if"Realtime Currency Exchange Rate" not in data:
        raise HTTPException(status_code=400, detail="Realtime Currency Exchange Rate not in response")
    
    exchange_rate = float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
    return price * exchange_rate


async def async_converter(from_currency: str, to_currencies: str, price: float):
    url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currencies}&apikey={APIKEY}'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                data = await response.json()
    except Exception as error:
        raise HTTPException(status_code=400, detail=error)
    
    if"Realtime Currency Exchange Rate" not in data:
        raise HTTPException(status_code=400, detail=f"Realtime Currency Exchange Rate not in response{data}")
    
    exchange_rate = float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
    return {to_currencies: price * exchange_rate}
    