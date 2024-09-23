# dao/local/local_dao.py

from abc import ABC, abstractmethod

class LocalDao(ABC):
    @abstractmethod
    def save_product_details(self, products):
        """Save product details in local storage."""
        pass
