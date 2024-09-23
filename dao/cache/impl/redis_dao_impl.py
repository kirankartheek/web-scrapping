import redis
import json
from dao.cache.cache_dao import CacheDao
from dto.product_dto import ProductDto


class RedisDaoImpl(CacheDao):
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.Redis(host=host, port=port, db=db)

    async def save_product_details(self, key, product_dto: ProductDto):
        # Get the current product details from Redis
        current_product = self.redis_client.hgetall(product_dto.product_title)

        # Check if the key exists and if the price has changed
        if not current_product or current_product.get(b"price").decode('utf-8') != product_dto.product_price:
            # Store the complete product details in Redis
            self.redis_client.hset(product_dto.product_title, mapping={
                "price": product_dto.product_price,
                "image": product_dto.path_to_image,
                "name": product_dto.product_title  # Saving the name for consistency
            })
            # print(f"Saved/Updated product: {product_dto.name} with price: {product_dto.price}")
