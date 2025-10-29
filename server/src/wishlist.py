import csv 

class Wishlist:
    def __init__(self, csv_file: str):
        self.csv_file = csv_file

    def load_wishlist(self) -> list[str]:
        wishlist_items = []

        with open(self.csv_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    wishlist_items.append(row[0])

        return wishlist_items