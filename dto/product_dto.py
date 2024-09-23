class ProductDto:
    def __init__(self, name: str, price: str, image: str):
        self.product_title = name
        self.product_price = price
        self.path_to_image = image

    def to_dict(self):
        return {
            "product_title": self.product_title,
            "product_price": self.product_price,
            "path_to_image": self.path_to_image
        }
