from ultralytics import YOLO
import cv2

# Map generic YOLO labels to specific grocery items
LABEL_MAP = {
    'bottle': ['milk', 'juice'],
    'bowl': ['salad', 'soup'],
    'cup': ['beverage'],
    # You can add more specific mappings here
}

MODEL_PATH = "yolov8n.pt"
CONFIDENCE = 0.35

class AI_Image_Detection:
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.model = YOLO(MODEL_PATH)

    def item_detection(self) -> tuple[list[str], str]:
        # Run inference
        results = self.model.predict(source=self.image_path, conf=CONFIDENCE)
        record = results[0]
        items_detected = []

        # Extract detected class names
        for box in record.boxes:
            confidence_score = (box.conf.cpu().numpy())
            if confidence_score >= CONFIDENCE:
                class_id = int(box.cls.cpu().numpy())
                item_name = self.model.names[class_id]
                items_detected.append(item_name)
        
        # FIX: Don't discard items! 
        # If item is in map, extend with specific ingredients.
        # If NOT in map, keep the original label (e.g., "apple", "pizza").
        extended_label = [] 
        for label in items_detected:
            # Skip 'refrigerator' as it's not a food item
            if label == 'refrigerator':
                continue
                
            # Use mapping if exists, otherwise wrap the label in a list
            extended_items = LABEL_MAP.get(label, [label])
            extended_label.extend(extended_items)
        
        # Save annotated image
        annotated_image = record.plot()
        annotated_image_path = "fridge_detected.jpg"
        cv2.imwrite(annotated_image_path, annotated_image)

        # Return unique items
        return list(set(extended_label)), annotated_image_path