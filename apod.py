import requests
import api_key

url = "https://api.nasa.gov/planetary/apod?api_key="

r = requests.get(url + api_key.api_key)

print(r.json()["title"])


