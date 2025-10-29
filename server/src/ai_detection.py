from ultralytics import YOLO
import cv2

LABEL_MAP = {
    'bottle': ['milk', 'orange juice'],
    'apple': ['apple'],
    'bowl': ['lettuce', 'tomato', 'cheese'],
    'banana': ['banana'],
    'refrigerator': [],  
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