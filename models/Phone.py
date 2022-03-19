class Phone:
    def __init__(self, brand, name, price, announcement_year, display_size, memory, os):
        self.brand = brand
        self.name = name
        self.price = price
        self.announcement_year = announcement_year
        self.display_size = display_size
        self.memory = memory
        self.os = os

    def get_phone_features(self):
        features = {
            "brand": self.brand,
            "name": self.name,
            "price": self.price,
            "announcement_year": self.announcement_year,
            "display_size": self.display_size,
            "memory": self.memory,
            "os": self.os,
        }
        return features
