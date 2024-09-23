import redis
import json
from dao.cache.cache_dao import CacheDao
from dto.product_dto import ProductDto


class RedisDaoImpl(CacheDao):
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.Redis(host=host, port=port, db=db)

    def save_product_details(self, key, product_dto: ProductDto):
        # Convert the value dictionary to a JSON string
        value_json = json.dumps(product_dto.to_dict())

        # Retrieve the current value from Redis
        current_value = self.redis_client.get(key)

        # Compare current value with new value
        if current_value is None or current_value.decode('utf-8') != value_json:
            # Only update if the value has changed
            self.redis_client.set(key, value_json)
            print(f"Updated Redis key: {key}")
