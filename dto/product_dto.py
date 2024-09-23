class ProductDto:
    def __init__(self, name: str, price: str, image: str):
        self.name = name
        self.price = price
        self.image = image

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "image": self.image
        }
