import json

class ProductsDao:
    def save_to_json(self, data):
        with open("scraped_data.json", "w") as file:
            json.dump(data, file, indent=4)
