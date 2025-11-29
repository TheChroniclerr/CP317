import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

# Import the custom classes
# Ensure ai_detection.py, wishlist.py, comparison.py AND grocery_api.py are in the same directory
from ai_detection import AI_Image_Detection
from wishlist import Wishlist
from comparison import Comparison
from grocery_api import make_api_call

app = Flask(__name__)

# --- Configuration ---
# Create a folder named 'uploads' in the same directory if it doesn't exist
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit upload size to 16MB

# Supported file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'}

# Simple in-memory list to track items (uploaded filenames)
items_list = []

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Method 1: GET method to list items ---
@app.route('/', methods=['GET'])
def index():
    """Returns a JSON list of uploaded items."""
    return jsonify({"files": items_list})

# --- Method 2: POST method to upload a file ---
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        items_list.append(filename)
        
        return jsonify({"message": "File uploaded successfully", "filename": filename}), 201
    
    return jsonify({"error": "Invalid file type"}), 400

# --- Method 3: Route to trigger AI Detection ---
@app.route('/detect/<filename>', methods=['GET'])
def detect_items(filename):
    if not allowed_file(filename):
        return jsonify({"error": "Invalid filename format"}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found. Please upload it first."}), 404

    try:
        detector = AI_Image_Detection(file_path)
        detected_items, annotated_image_path = detector.item_detection()
        
        return jsonify({
            "message": "Detection completed successfully",
            "detected_items": detected_items,
            "annotated_image_saved_at": annotated_image_path
        }), 200

    except Exception as e:
        return jsonify({"error": f"AI Detection failed: {str(e)}"}), 500

# --- Method 4: Route to Compare Detection with Wishlist & Find Prices ---
@app.route('/compare/<image_filename>/<csv_filename>', methods=['GET'])
def compare_detection_with_wishlist(image_filename, csv_filename):
    """
    1. Detects items in image.
    2. Compares with wishlist CSV.
    3. Searches for MISSING items using Grocery API.
    """
    # 1. Validate paths
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image_filename))
    csv_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(csv_filename))

    if not os.path.exists(image_path) or not os.path.exists(csv_path):
        return jsonify({"error": "One or both files not found. Please upload them first."}), 404

    try:
        # 2. Run AI Detection
        detector = AI_Image_Detection(image_path)
        detected_items, _ = detector.item_detection() 

        # 3. Load Wishlist
        wishlist_loader = Wishlist(csv_path)
        wishlist_items = wishlist_loader.load_wishlist()

        # 4. Run Comparison
        comparator = Comparison(detected_items, wishlist_items)
        found_in_fridge, missing_from_fridge = comparator.compare_items()

        # 5. Find Shopping Options for Missing Items
        shopping_data = {}
        
        # NOTE: This loop runs synchronously. If you have many missing items, 
        # this request might take a long time to complete.
        for item in missing_from_fridge:
            try:
                # Call the external API function
                min_price_walmart, min_price_amazon, link_walmart, link_amazon = make_api_call(item)
                
                shopping_data[item] = {
                    "walmart": {
                        "price": min_price_walmart,
                        "link": link_walmart
                    },
                    "amazon": {
                        "price": min_price_amazon,
                        "link": link_amazon
                    }
                }
            except Exception as api_error:
                # Handle API errors gracefully so we don't crash the whole response
                shopping_data[item] = {
                    "error": f"Could not fetch data: {str(api_error)}"
                }

        return jsonify({
            "analysis": {
                "items_detected_in_image": detected_items,
                "items_in_wishlist": wishlist_items
            },
            "results": {
                "available": found_in_fridge,
                "missing": missing_from_fridge
            },
            "shopping_options": shopping_data
        }), 200

    except Exception as e:
        return jsonify({"error": f"Process failed: {str(e)}"}), 500

if __name__ == '__main__':
    print(f"Server starting. Uploads will be saved to: {os.path.abspath(UPLOAD_FOLDER)}")
    app.run(debug=True, port=5000)