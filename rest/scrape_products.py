from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel, Field, validator, field_validator

from service.products_scrapper import ProductsScrapper
from config import config
from utils.validation import validate_token

router = APIRouter()

# Request model
class ScrapeRequest(BaseModel):
    pageLimit: int =  Field(None, description="The number of pages to scrape (must be greater than or equal to 1 and default value is set to 200)")
    proxy: str = Field(None, description="The proxy string to use for scraping (optional)")

    @field_validator('pageLimit')
    def validate_page_limit(cls, v):
        if v is not None and v <= 0:
            raise ValueError('pageLimit must be greater than 0 if provided')
        return v

    @field_validator('proxy')
    def validate_proxy(cls, v):
        if v is not None and not isinstance(v, str):
            raise ValueError('Proxy must be a string')
        return v

# Response model
class ScrapeResponse(BaseModel):
    success: bool
    total_count: int

# API endpoint
@router.post("/scrape/products", response_model=ScrapeResponse)
async def scrape_catalogue(request: ScrapeRequest, token: str = Header(...)):
    scraper_service = ProductsScrapper()
    success, total_count = scraper_service.scrape_data(request.pageLimit, request.proxy)
    if success:
        print(f"Total Products Scrapped : {total_count}")
    return ScrapeResponse(success=success, total_count=total_count)
