from ai_detection import AI_Image_Detection
from wishlist import Wishlist
from comparison import Comparison
import os

def main():
    
    image_path = os.path.join(os.path.dirname(__file__), "fridge.jpg")
    wishlist_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mywishlist.csv")
    detector = AI_Image_Detection(image_path)
    detected_items, annotated_image_path = detector.item_detection()
    

    print("Detected items image saved to:", annotated_image_path)


    get_wishlist = Wishlist(wishlist_path)
    wishlist_items = get_wishlist.load_wishlist()
    print("Wishlist items:", wishlist_items)


    comparer = Comparison(detected_items, wishlist_items)
    found_items, missing_items = comparer.compare_items()
    print("Detected items:", detected_items)
    print("Found items:", found_items)
    print("Missing items:", missing_items)

if __name__ == "__main__":
    main()