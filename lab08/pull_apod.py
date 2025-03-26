import requests

API_KEY = "vTzUJbik7sb0OmImpgcy8un14gKb7h3C9Bi1nG4M"
BASE_URL = "https://api.nasa.gov/planetary/apod"

def fetch_apod(date=None):
    ''' Pull image and data from NASA's website'''
    params = {"api_key": API_KEY}
    if date:
        params["date"] = date
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch APOD: {response.status_code}")