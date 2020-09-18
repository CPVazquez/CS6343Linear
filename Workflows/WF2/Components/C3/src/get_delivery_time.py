import requests
import json
from config import API_KEY
import heapq
 
URL = "https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&key={}"

def _convert_time_str(time):
    time = time.split()        
    if len(time) > 2:
        mins = int(time[2])
        hours = int(time[0])
    else:
        mins = int(time[0])
        hours = 0
    return hours * 60 + mins    

def _get_time(origin, destination):
    url = URL.format(origin, destination, API_KEY)    
    response = requests.get(url)
    content = json.loads(response.content.decode())    
    time = (content['routes'][0]['legs'][0]['duration']['text'])        
    return _convert_time_str(time)

def get_delivery_time(origin, destination, delivery_entities):
    origin = ",".join(map(str, origin))
    destination = ",".join(map(str, destination))
    delivery_entities = [",".join(map(str, coordinates)) for coordinates in delivery_entities]    

    best_time = float('inf')
    best_entity = 0
    for idx, delivery_entity in enumerate(delivery_entities):        
        time = _get_time(delivery_entity, origin)                
        if time < best_time:
            best_time = time
            best_entity = idx

    return _get_time(origin, destination) + best_time, best_entity

if __name__ == "__main__":
    store = (32.984363, -96.749689) #utd
    customer = (32.998323, -96.775618) #pearl on frankford
    delivery_entities = [(32.993394, -96.768680), (32.998795, -96.734466), (32.988504, -96.770228)] #palencia, marquis, chatham
    print(get_delivery_time(store, customer, delivery_entities))
        
    
