from abc import ABC, abstractmethod

class CacheDao(ABC):
    @abstractmethod
    def save_product_details(self, key: str, product):
        """Save product details in the cache."""
        pass