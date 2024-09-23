import json
import os
from dao.local.local_dao import LocalDao

class JsonDaoImpl(LocalDao):
    def __init__(self, filename='products.json'):
        self.filename = filename

    def save_product_details(self, products):
        with open(self.filename, 'w') as f:
            json.dump([product.to_dict() for product in products], f)
