import requests
API_URL = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": "Bearer your_api key"}
payload = {"inputs": "how descovred gravity."}
response = requests.post(API_URL, headers=headers, json=payload)
print(response.json())

