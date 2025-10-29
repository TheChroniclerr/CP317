from ultralytics import YOLO
import cv2
'''
LABEL_MAP = {
    'bottle': ['milk', 'orange juice'],
    'apple': ['apple'],
    'bowl': ['lettuce', 'tomato', 'cheese'],
    'banana': ['banana'],
    'refrigerator': [],  
}
'''
LABEL_MAP = {
    # Bottles & Drinks
    'bottle': ['milk', 'orange juice', 'apple juice', 'water', 'soda', 'yogurt drink', 'smoothie', 'wine', 'beer'],
    'can': ['soda', 'beer', 'energy drink', 'juice can'],

    # Fruits (YOLO often confuses colors/shapes)
    'apple': ['apple', 'green apple', 'red apple'],
    'orange': ['orange', 'mandarin', 'tangerine'],
    'banana': ['banana'],
    'grape': ['grapes', 'red grapes', 'green grapes'],
    'strawberry': ['strawberry'],
    'blueberry': ['blueberry'],
    'kiwi': ['kiwi'],
    'melon': ['watermelon', 'cantaloupe', 'honeydew'],
    'pear': ['pear'],
    'pineapple': ['pineapple'],
    'mango': ['mango'],

    # Vegetables (YOLO often detects bowl/cup instead of vegetable)
    'tomato': ['tomato', 'cherry tomato'],
    'lettuce': ['lettuce', 'romaine', 'iceberg'],
    'cucumber': ['cucumber'],
    'carrot': ['carrot'],
    'bell pepper': ['red bell pepper', 'green bell pepper', 'yellow bell pepper'],
    'onion': ['onion', 'red onion', 'green onion'],
    'garlic': ['garlic'],
    'potato': ['potato', 'sweet potato'],
    'broccoli': ['broccoli'],
    'cauliflower': ['cauliflower'],
    'spinach': ['spinach'],
    'cabbage': ['cabbage', 'red cabbage'],

    # Dairy & Eggs
    'cheese': ['cheese', 'cheddar', 'mozzarella', 'parmesan', 'feta'],
    'egg': ['egg', 'eggs'],
    'butter': ['butter', 'margarine'],
    'yogurt': ['yogurt', 'greek yogurt', 'plain yogurt'],

    # Meat & Fish
    'meat': ['chicken', 'beef', 'pork', 'bacon', 'ham', 'turkey'],
    'fish': ['salmon', 'tuna', 'cod', 'shrimp'],

    # Snacks & Misc
    'bread': ['bread', 'baguette', 'whole wheat bread'],
    'chips': ['chips', 'tortilla chips'],
    'nuts': ['almonds', 'cashews', 'peanuts', 'mixed nuts'],
    'bowl': ['salad', 'fruit mix', 'veggie mix', 'cheese'],
    'cup': ['coffee', 'tea', 'milk'],

    # Ignore irrelevant YOLO labels
    'refrigerator': [],
    'sink': [],
    'knife': [],
    'spoon': [],
    'fork': [],
    'bowl': ['lettuce', 'tomato', 'cheese'], # sometimes YOLO labels vegetables as bowl
}


MODEL_PATH = "yolov8n.pt"
CONFIDENCE = 0.35
class AI_Image_Detection:
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.model = YOLO(MODEL_PATH)

    def item_detection(self) -> list[str]:
        results = self.model.predict(source=self.image_path, conf=CONFIDENCE)
        record = results[0]
        items_detected = []

        for box in record.boxes:
            confidence_score = (box.conf.cpu().numpy())
            if confidence_score >= CONFIDENCE:
                class_id = int(box.cls.cpu().numpy())
                item_name = self.model.names[class_id]
                items_detected.append(item_name)
        
        extended_label = [] 
        for label in items_detected:
            extended_items = LABEL_MAP.get(label, [])
            extended_label.extend(extended_items)
        
        annotated_image = record.plot()
        annotated_image_path = "fridge_detected.jpg"
        cv2.imwrite(annotated_image_path, annotated_image)

        
        
        return list(set(extended_label)), annotated_image_path 