import requests
import json

url = "http://127.0.0.1:8081/gen_image/"

payload = json.dumps({
  "prompt": "string",
  "width_image": 512,
  "height_image": 512
})
headers = {
  'accept': 'application/json',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
response = response.json()

print(response['prompt'])

import requests
import json

url = "http://127.0.0.1:8081/load_models/"

payload = json.dumps({
  "device": "cuda",
  "torch_dtype": 16,
  "num_inference_steps": 50,
  "checkpoint_name": "stabilityai/stable-diffusion-2-1"
})
headers = {
  'accept': 'application/json',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)