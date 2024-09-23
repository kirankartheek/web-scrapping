import requests
from bs4 import BeautifulSoup
import json
from config.config import RETRY_LIMIT
from dao.products_dao import ProductsDao
from config import config
from time import sleep


class ProductsScrapper:
    def __init__(self):
        self.base_url = "https://dentalstall.com/shop/page/"
        self.productsDao = ProductsDao()

    def scrape_data(self, page_limit: int, proxy: str = None):
        all_products = []
        proxies = {"http": proxy, "https": proxy} if proxy else None
        total_count = 0
        for page in range(1, page_limit + 1):
            url = f"{self.base_url}{page}/"
            retries = 0
            while retries < RETRY_LIMIT:
                try:
                    response = requests.get(url, proxies=proxies, timeout=5)
                    response.raise_for_status()  # Raise error if status is not 200
                    soup = BeautifulSoup(response.content, "html.parser")
                    products = self._parse_page(soup)
                    total_count += len(products)
                    all_products.extend(products)
                    break
                except requests.RequestException as e:
                    retries += 1
                    sleep(2)  # Simple retry backoff
                    if retries == RETRY_LIMIT:
                        return False, total_count  # Return if all retries fail

        # Save to local storage
        self.productsDao.save_to_json(all_products)
        return True, total_count

    def _parse_page(self, soup: BeautifulSoup):
        products = []
        items = soup.select(".product")  # Modify based on the website's HTML structure
        for item in items:
            try:
                name = item.select_one(".woo-loop-product__title").text.strip()

                # Extract product price
                price = item.select_one(".woocommerce-Price-amount").text.strip()
                price = price.replace("₹", "").strip()

                # Extract product image URL
                image = item.select_one("img")["data-lazy-src"]  # Use data-lazy-src for lazy-loaded images

                products.append({"name": name, "price": price, "image": image})
            except Exception as e:
                print(f"Error parsing product: {e}")  # Log any errors
        return products
