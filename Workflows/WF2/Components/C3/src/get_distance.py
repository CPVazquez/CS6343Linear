import requests
import json

API_KEY = "AIzaSyDlgFOUYH7vVFyX8IRYr_BrJ7MqKq5aisM" 
URL = "https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&key={}"

def get_distance(origin, destination):
    origin = ",".join(map(str, origin))
    destination = ",".join(map(str, destination))
    url = URL.format(origin, destination, API_KEY)    
    response = requests.get(url)
    content = json.loads(response.content.decode())
    distance = (content['routes'][0]['legs'][0]['distance']['text']).split()
    return float(distance[0]), distance[1]

if __name__ == "__main__":
    origin = (32.9982, -96.7756)
    destination = (32.9858, -96.7501)
    print(get_distance(origin, destination))
        
    
