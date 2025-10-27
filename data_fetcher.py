import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_data(animal_name):
    global response
    api_key = os.environ.get("API_KEY")
    if not api_key:
        print("Error!!! dotenv not found")
        print("Please create dotenv file, and try it again")
        return None

    api_url = f"https://api.api-ninjas.com/v1/animals?name={animal_name}"
    headers = {"X-Api-Key": api_key}

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Fehler bei der API-Anfrage: {e}")
        if 'response' in locals() and response is not None:
            print(f"Server-Antwort: {response.text}")
        return None

