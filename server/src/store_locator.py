import requests
class StoreLocator:
    def __init__(self, user_address: str):
        self.user_latitude, self.user_longitude = self.get_address(user_address)
        self.osrm_url = "http://router.project-osrm.org/route/v1/driving/"
    
    def get_address(self, address):
        url = "https://nominatim.openstreetmap.org/search" 

        search_query = {"q": address, "format": "json", "limit": 1}

        headers = {"User-Agent": "FillrUpApp/1.0"}

        response = requests.get(url, params=search_query, headers=headers)

        
        data = response.json()

        latitude = float(data[0]["lat"])
        longitude = float(data[0]["lon"])
        
        return latitude, longitude
       
        
    def get_coordinates(self, store_name):

        url = "https://nominatim.openstreetmap.org/search" 

        search_query = {"q": store_name, "format": "json", "limit": 5, "viewbox": f"{self.user_longitude-0.5},{self.user_latitude-0.5},{self.user_longitude+0.5},{self.user_latitude+0.5}", "bounded": 1}

        headers = {"User-Agent": "FillrUpApp/1.0"}

        response = requests.get(url, params=search_query, headers=headers)

        
        data = response.json()
        

        if not data:
            return []
        
        coords = []

        for store in data:
            latitude = float(store["lat"])
            longitude = float(store["lon"])

            address = store.get("display_name", "")
            
            coords.append((latitude, longitude, address))

        return coords
    
    def get_route(self, store_latitude, store_longitude):
        url = f"{self.osrm_url}{self.user_longitude},{self.user_latitude};{store_longitude},{store_latitude}?overview=false"
        response = requests.get(url)
        data = response.json()

        if "routes" not in data or not data["routes"]:
            return None
        
        route = data["routes"][0]

        return {"distance_km": route["distance"] / 1000, "duration_min": route["duration"]/60 }
    
    def nearest_store(self, store_name):

        store_coords = self.get_coordinates(store_name)

        if not store_coords:
            return {"error": f"Could not find any {store_name} nearby"}

        nearest = None
        shortest_dist = float("inf")

        for (lat, lon, address) in store_coords:
            route = self.get_route(lat,lon)

            if route and route["distance_km"] < shortest_dist:
                shortest_dist = route["distance_km"]
                nearest = {"store": store_name, "address": address, "latitude": lat, "longitude": lon, "distance_km": route["distance_km"], "duration_min": route["duration_min"]}
            
        if not nearest:
            return {"error": f"Could not calculate route"}
        return nearest 
    


