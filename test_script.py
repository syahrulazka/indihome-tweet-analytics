# Test the API using curl or Python requests

# 1. Single prediction
import requests

url = "http://localhost:8000/predict"
data = {"text": "yah mulai dah lemotnya ni internet indihome"}
response = requests.post(url, json=data)
print(response.json())

# 2. Batch prediction
url = "http://localhost:8000/predict_batch"
data = {
    "texts": [
        "kenapa ya internet indihome sering lemot?",
        "koneksi internet indihome sangat cepat dan stabil",
        "bales dm dong, internet indihome ini kenapa ya?",
    ]
}
response = requests.post(url, json=data)
print(response.json())

# 3. Health check
response = requests.get("http://localhost:8000/health")
print(response.json())

# 4. Model info
response = requests.get("http://localhost:8000/model_info")
print(response.json())