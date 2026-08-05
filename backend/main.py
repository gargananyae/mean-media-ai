from fastapi import FastAPI
from pydantic import BaseModel

from backend.crawler.crawler import crawl

app = FastAPI(
    title="Mean Media AI",
    description="AI-powered SEO & GEO Intelligence Platform",
    version="0.1.0"
)

class Website(BaseModel):
    url: str

@app.get("/")
def home():
    return {
        "message": "Welcome to Mean Media AI 🚀"
    }

@app.post("/analyze")
def analyze(website: Website):

    data = crawl(website.url)

    return data