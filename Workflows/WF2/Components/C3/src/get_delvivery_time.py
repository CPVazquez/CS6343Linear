import requests
import json
from config import API_KEY
 
URL = "https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&key={}"

def _convert_time_str(time):
    time = time.split()    
    print(time)
    if len(time) > 2:
        mins = int(time[2])
        hours = int(time[0])
    else:
        mins = int(time[0])
        hours = 0
    return hours * 60 + mins    

def get_time(origin, destination):
    origin = ",".join(map(str, origin))
    destination = ",".join(map(str, destination))
    url = URL.format(origin, destination, API_KEY)    
    response = requests.get(url)
    content = json.loads(response.content.decode())    
    time = (content['routes'][0]['legs'][0]['duration']['text'])        
    return _convert_time_str(time)

if __name__ == "__main__":
    origin = (32.9982, -96.7756)
    destination = (32.9858, -96.7501)    
    print(get_time(origin, destination))
        
    
