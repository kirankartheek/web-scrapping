from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, validator
from service.products_scrapper import ProductsScrapper
from config import config
from utils.validation import validate_token

router = APIRouter()

# Request model
class ScrapeRequest(BaseModel):
    pageLimit: int = Field(..., gt=0, description="The number of pages to scrape (must be greater than 0)")
    proxy: str = Field(None, description="The proxy string to use for scraping (optional)")

    @validator('proxy')
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
async def scrape_catalogue(request: ScrapeRequest, token: str = Depends(validate_token)):
    scraper_service = ProductsScrapper()
    success, total_count = scraper_service.scrape_data(request.pageLimit, request.proxy)
    return ScrapeResponse(success=success, total_count=total_count)
