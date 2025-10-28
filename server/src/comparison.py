class Comparison:
    def __init__(self, items_detected: list[str], wishlist_items: list[str]):
        self.items_detected = items_detected
        self.wishlist_items = wishlist_items
    
    def compare_items(self):

        found = []
        missing = []

        for wishlist_item in self.wishlist_items:
            matched = False
            for detected_item in self.items_detected:
                if wishlist_item.lower() in detected_item.lower():
                    found.append(wishlist_item)
                    matched = True
                    break
            if not matched:
                missing.append(wishlist_item)
        
        return found, missing

    