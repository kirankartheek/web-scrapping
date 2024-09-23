from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from rest.scrape_products import router as scrape_products

app = FastAPI()


# @app.get("/scrape")
# async def scrape(url: str):
#     # Fetch the web page
#     response = requests.get(url)
#     if response.status_code == 200:
#         # Parse the HTML content using BeautifulSoup
#         soup = BeautifulSoup(response.content, "html.parser")
#
#         # Example: Extract the page title
#         page_title = soup.title.string if soup.title else "No title found"
#
#         return {"page_title": page_title}
#     else:
#         return {"error": "Failed to retrieve the page"}


app.include_router(scrape_products, prefix="/api")
