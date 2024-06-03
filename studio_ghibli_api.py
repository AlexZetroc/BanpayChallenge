import requests

BASE_URL = "https://ghibliapi.vercel.app"

def fetch_data_by_role(role):
    endpoints = {
        'films': '/films',
        'people': '/people',
        'locations': '/locations',
        'species': '/species',
        'vehicles': '/vehicles'
    }
    if role not in endpoints:
        return {'message': 'Invalid role'}, 400
    response = requests.get(f"{BASE_URL}{endpoints[role]}")
    if response.status_code == 200:
        return response.json(), 200
    return {'message': 'Failed to fetch data'}, response.status_code
