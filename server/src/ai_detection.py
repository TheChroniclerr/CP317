from ultralytics import YOLO
import cv2
import os

# Gets the model path to the trained detection model 
MODEL_PATH = os.path.join(os.path.dirname(__file__), "best.pt")

# Confidence threshold for detections
CONFIDENCE = 0.35

class AI_Image_Detection:
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.model = YOLO(MODEL_PATH)

    def item_detection(self) -> list[str]:
        
        results = self.model.predict(source=self.image_path, conf=CONFIDENCE) 
        record = results[0] 
        items_detected = []

        # Iterates through detected boxes and filters by confidence score 
        for box in record.boxes:
            confidence_score = (box.conf.cpu().numpy()) # Get confidence score
            if confidence_score >= CONFIDENCE: 
                class_id = int(box.cls.cpu().numpy()) # Get class ID
                item_name = self.model.names[class_id] # Get item name from class ID
                items_detected.append(item_name) # Append detected item name to the list
        
        
        # Save annotated image with detected boxes
        annotated_image = record.plot()
        annotated_image_path = "fridge_detected.jpg"
        cv2.imwrite(annotated_image_path, annotated_image)

        
        # Returns list of detected items and path to annotated image 
        return list(set(items_detected)), annotated_image_path 