import requests

# Replace with your actual API key
API_KEY = '4c8c315f5eaf4c9a8cfb2f8e1c5538ca'
API_URL = f'https://api.spoonacular.com/recipes/random?apiKey={API_KEY}&includeNutrition=true&number=5'

# Send the request to the API
response = requests.get(API_URL)

# Check if the response is successful
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}")
