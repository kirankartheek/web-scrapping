import asyncio

import requests
from bs4 import BeautifulSoup
import json
from config.config import RETRY_LIMIT, RETRY_INTERVAL
from dao.cache.impl.redis_dao_impl import RedisDaoImpl
from dao.local.impl.json_dao_impl import JsonDaoImpl
from config import config
from time import sleep

from dto.product_dto import ProductDto


class ProductsScrapper:
    def __init__(self):
        self.base_url = "https://dentalstall.com/shop/page/"
        self.cache = RedisDaoImpl()
        self.local_storage = JsonDaoImpl()

    def scrape_data(self, page_limit: int, proxy: str = None):
        all_products = []
        proxies = {"http": proxy, "https": proxy} if proxy else None
        total_count = 0
        print("Starting the scraping process...")
        page = 1
        encountered_404 = False  # Track if 404 was encountered

        # If page_limit is None, scrape till the last page
        while page_limit is None or page <= page_limit:
            url = f"{self.base_url}{page}/"
            retries = 0
            response = None  # Initialize response to None

            while retries < RETRY_LIMIT:
                try:
                    response = requests.get(url, proxies=proxies, timeout=5)

                    # Check for 404 status to stop scraping more pages
                    if response.status_code == 404:
                        print(f"Page not found (404) encountered on page {page}. Stopping further page scraping.")
                        encountered_404 = True  # Mark that 404 is encountered
                        break  # Break out of the loop, but continue saving the products

                    response.raise_for_status()  # Raise error if status is not 200
                    soup = BeautifulSoup(response.content, "html.parser")

                    # Parse the products
                    print(f"Page being scraped... {page}")
                    products = self._parse_page(soup)
                    total_count += len(products)
                    all_products.extend(products)
                    break  # Exit the retry loop on success

                except requests.HTTPError as http_err:
                    if response is not None and response.status_code == 404:
                        # Stop further scraping if 404 encountered
                        print(f"404 error on page {page}, stopping further scraping.")
                        encountered_404 = True
                        break  # Break the retry loop if 404 is encountered
                    else:
                        retries += 1
                        print(f"HTTP error occurred on page {page}: {http_err}")
                        sleep(RETRY_INTERVAL)  # Retry after a delay
                        if retries == RETRY_LIMIT:
                            return False, 0  # Stop if all retries fail

                except requests.RequestException as e:
                    retries += 1
                    print(f"Request error on page {page}: {e}")
                    sleep(RETRY_INTERVAL)
                    if retries == RETRY_LIMIT:
                        return False, 0  # Stop if all retries fail

            # Stop fetching new pages if 404 encountered
            if encountered_404:
                break

            page += 1

        print("data scraping finished.")
        # Save to local storage after scraping is complete
        self.local_storage.save_product_details(all_products)

        print("data saved to local file.")

        # Save to cache after scraping is complete
        for product in all_products:
            asyncio.create_task(self.cache.save_product_details(product.product_title, product))

        print("data saved to redis cache")

        return True, total_count



    def _parse_page(self, soup: BeautifulSoup):
        products = []
        items = soup.select(".product")  # Modify based on the website's HTML structure
        for item in items:
            try:
                # Extract product name
                name = item.select_one(".woo-loop-product__title")
                if not name:
                    # Skip if name is not present
                    print("Skipping due to name not being present")
                    continue
                name = name.text.strip()

                # Extract product price
                price = item.select_one(".woocommerce-Price-amount")
                if price:
                    price = price.text.strip().replace("₹", "").strip()
                else:
                    price = "-1"  # Set price to -1 if not available


                # Extract product image URL (optional, default to empty string if not found)
                image = item.select_one("img")
                if image:
                    image = image.get("data-lazy-src", "").strip()  # Get 'data-lazy-src' or set to ""
                else:
                    image = ""  # Set image to empty string if not available

                product_dto = ProductDto(name=name, price=price, image=image)
                products.append(product_dto)
            except Exception as e:
                print(f"Error parsing product: {item} with Exception {e}")  # Log any errors
        return products
