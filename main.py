from fastapi import FastAPI
import requests
from config import API_KEY
from database import get_db_connection

app = FastAPI()

FINNHUB_URL = "https://finnhub.io/api/v1/quote"

@app.get("/fetch_stock/{symbol}")
def fetch_stock(symbol: str):
    params = {"symbol": symbol, "token": API_KEY}
    response = requests.get(FINNHUB_URL, params=params)
    
    if response.status_code != 200:
        return {"error": "Failed to fetch stock data"}
    
    data = response.json()
    
    # MySQL에 데이터 저장
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO stock_data (symbol, current_price, price_change, percent_change, 
                            high_price, low_price, open_price, prev_close, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (symbol, data["c"], data["d"], data["dp"], data["h"], 
              data["l"], data["o"], data["pc"], data["t"])

    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"message": "Stock data saved", "data": data}
