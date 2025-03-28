
from fastapi import FastAPI
from pymongo import MongoClient
from typing import List
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

# MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")  # MongoDB 연결
db = client["news_database"]  # 새로운 데이터베이스 이름 'news'
collection = db["yahoo_news"]  # 새로운 컬렉션 이름 'yahoo'

# FastAPI 인스턴스 생성
app = FastAPI()

# 뉴스 데이터 모델 (응답 포맷)
class NewsItem(BaseModel):
    title: str
    link: str
    date: str
    content: str
    image: str

@app.get("/check_connection")
def check_connection():
    try:
        # MongoDB에서 데이터베이스 목록을 가져오는 쿼리
        databases = client.list_database_names()
        return {"message": f"Connected to MongoDB. Databases: {databases}"}
    except Exception as e:
        return {"message": f"Failed to connect to MongoDB. Error: {str(e)}"}

# 뉴스 목록 조회 API
@app.get("/news", response_model=List[NewsItem])
def get_news():
    news_items = list(collection.find({}, {"_id": 0}))  # MongoDB에서 뉴스 가져오기
    return news_items

# 크롤러 실행 API
@app.get("/crawl")
def crawl_news():
    from crawler import fetch_yahoo_news, save_to_mongo

    news_items = fetch_yahoo_news()  # 뉴스 크롤링
    save_to_mongo(news_items)  # MongoDB에 저장
    return {"message": f"{len(news_items)} articles crawled and saved."}
