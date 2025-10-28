import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from ai_detection import AI_Image_Detection
from wishlist import Wishlist
from comparison import Comparison
import tempfile

load_dotenv()

api = Flask(__name__)

@api.route("/detect", methods=["POST"])

def detect_items():

    if "image" not in request.files or "wishlist" not in request.files:
        return jsonify({"error": "Image and Wishlist files are required."}), 400
    
    image_file = request.files["image"]
    wishlist_file = request.files["wishlist"]

    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_image:
        image_path = temp_image.name
        image_file.save(image_path)
    
    try:
        detector = AI_Image_Detection(image_path)
        items_detected = detector.item_detection()
    except Exception as e:
        return jsonify({"error": f"Item detection failed: {str(e)}"}), 500
    finally:
        if os.path.exists(image_path):
            os.remove(image_path)

    

    wishlist_items = Wishlist.load_wishlist(wishlist_file)
    comparison = Comparison(items_detected, wishlist_items)
    found, missing = comparison.compare_items()

    return jsonify({
        
        "items_detected": items_detected,
        "found_items": found,
        "missing_items": missing
    }), 200

if __name__ == "__main__":
    api.run(debug=True)


