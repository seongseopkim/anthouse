import requests
from config import API_KEY

def get_stock_data(symbol: str):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    return {"error": "데이터 가져오기 실패"}
