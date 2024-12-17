import sys
import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from fastapi.testclient import TestClient
from cloud_function.crawl_news.local_news_crawler import app

client = TestClient(app)

def test_crawl_news():
    response = client.post("/crawl_news", params={"location": "Taichung"})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "articles" in response.json()

def test_get_news():
    response = client.get("/get_news", params={"location": "Taichung"})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "news" in response.json()

def test_delete_expired_news():
    response = client.delete("/delete_expired_news")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "deleted_count" in response.json()
