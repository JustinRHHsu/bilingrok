from fastapi import FastAPI, HTTPException
from google.cloud import sql

app = FastAPI()

# Initialize Cloud SQL connection
def init_db():
    # ...existing code to initialize Cloud SQL connection...
    pass

@app.get("/get_news")
def get_news(location: str):
    try:
        db = init_db()
        # ...code to fetch news from Cloud SQL...
        news = []
        
        return {"status": "success", "news": news}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
