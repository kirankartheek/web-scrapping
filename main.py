from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from rest.scrape_products import router as scrape_products

app = FastAPI()

app.include_router(scrape_products, prefix="/api")
