from fuzzywuzzy import process

MATCH = 74
class Comparison:
    def __init__(self, items_detected: list[str], wishlist_items: list[str]):
        self.items_detected = items_detected
        self.wishlist_items = wishlist_items
    
    def compare_items(self):

        found = set()
        not_found = []

    
        
        for item in self.items_detected:
            match, score = process.extractOne(item, self.wishlist_items)
            
            if match and score >= MATCH:
                found.add(match)
        
        for item in self.wishlist_items:
            if item not in found:
                not_found.append(item)
        
        return list(found), not_found
    