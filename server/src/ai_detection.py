import os
import requests 


class AI_Image_Detection:
    def __init__(self, image_path: str):
        
        self.image_path = image_path
        self.api_key = os.getenv("LOGMEAL_API_KEY")
        self.endpoint = "https://api.logmeal.es/v2/recognition/complete"

    def item_detection(self) -> list[str]:
        
        if not self.api_key:
            raise ValueError("API key for LogMeal is not set in environment variables.")
        
        headers = {"Authorization": f"Bearer {self.api_key}"}

        with open(self.image_path, "rb") as image_file:
            files = {"image": image_file}
            response = requests.post(self.endpoint, headers = headers, files = files)

            if response.status_code != 200:
                raise RuntimeError(f"LogMeal API Request Failed: {response.status_code} - {response.text}")
            
            data = response.json()
            items_detected = []

            if "recognition_results" in data:
                for item in data["recognition_results"]:
                    if "name" in item:
                        items_detected.append(item["name"].lower())
        
        return list(set(items_detected))