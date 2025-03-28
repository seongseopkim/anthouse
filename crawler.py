from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

# MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["news"]  # 'news' 데이터베이스
collection = db["yahoo"]  # 'yahoo' 컬렉션

def fetch_yahoo_news():
    url = "https://news.yahoo.com/"  # Yahoo 뉴스 URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    articles = []
    for item in soup.find_all("article"):
        title = item.find("h3")
        link = item.find("a")
        date = item.find("time")
        content = item.find("p")
        image = item.find("img")
        
        if title and link:
            articles.append({
                "title": title.get_text(),
                "link": link["href"],
                "date": date.get_text() if date else "No Date",
                "content": content.get_text() if content else "No Content",
                "image": image["src"] if image else "No Image"
            })
    
    return articles

def save_to_mongo(news_items):
    # MongoDB에 뉴스 아이템 저장
    collection.insert_many(news_items)  # 'news' 데이터베이스의 'yahoo' 컬렉션에 뉴스 저장
