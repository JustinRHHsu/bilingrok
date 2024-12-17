# uvicorn news_and_events.local_news_crawler:app --reload

import os
from fastapi import FastAPI, HTTPException, Query
from datetime import datetime, timedelta
import pytz
import requests
from bs4 import BeautifulSoup
from google.cloud import firestore
from config.config import DB
import functions_framework

app = FastAPI()

# Initialize Firestore connection
def init_db():
    return DB.init_firestore_db()

@app.post("/crawl_news")
def crawl_news(location: str = Query(..., description="Location to search news for")):
    try:
        url = f"https://news.google.com/search?q={location}%20when%3A1d&hl=en-US&gl=US&ceid=US%3Aen"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract news articles
        articles = []
        print(f"start to crawl news")
        for item in soup.select('article'):
            title_tag = item.select_one('a.JtKRv')
            if title_tag:
                title = title_tag.text
                print(f"title: {title}")
                articles.append(title)
        
        # Save to Firestore
        db = init_db()
        utc_now = datetime.utcnow().replace(tzinfo=pytz.UTC)
        expire_time = utc_now + timedelta(days=1)
        doc_ref = db.collection('news_by_location').document(location)
        doc_ref.set({
            'location': location,
            'news_titles': articles,
            'crawl_time': utc_now,
            'expire_time': expire_time
        })
        
        return {"status": "success", "articles": articles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_news")
def get_news(location: str = Query(..., description="Location to get news for")):
    try:
        db = init_db()
        doc_ref = db.collection('news_by_location').document(location)
        doc = doc_ref.get()
        
        if doc.exists:
            news = doc.to_dict()
            if news['expire_time'].replace(tzinfo=pytz.UTC) > datetime.utcnow().replace(tzinfo=pytz.UTC):
                return {"status": "success", "news": news}
            else:
                return {"status": "error", "message": "No news found or news expired"}
        else:
            return {"status": "error", "message": "No news found or news expired"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete_expired_news")
def delete_expired_news():
    try:
        db = init_db()
        query = db.collection('news_by_location').where('expire_time', '<=', datetime.utcnow().replace(tzinfo=pytz.UTC))
        results = query.stream()
        
        deleted_count = 0
        for result in results:
            db.collection('news_by_location').document(result.id).delete()
            deleted_count += 1
        
        return {"status": "success", "deleted_count": deleted_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
