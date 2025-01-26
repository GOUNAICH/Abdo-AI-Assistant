import requests
import os

API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
headers = {"Authorization": "Bearer your_api_key_huggingface"}

def query(filename):
    try:
        if not os.path.exists(filename):
            raise FileNotFoundError(f"The file {filename} does not exist.")

        with open(filename, "rb") as f:
            data = f.read()
        response = requests.post(API_URL, headers=headers, data=data)
        response.raise_for_status() 

        return response.json()

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

file_path = r"img\photo.png"


output = query(file_path)
print(output)
