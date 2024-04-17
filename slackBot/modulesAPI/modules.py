import requests
import json

def setModel(device="cuda", torch_dtype=16, num_inference_steps=50,checkpoint_name="stabilityai/stable-diffusion-2-1"): 
    url = "http://models_service:8081/load_models/"

    payload = json.dumps({
    "device": device,
    "torch_dtype": torch_dtype,
    "num_inference_steps": num_inference_steps,
    "checkpoint_name": checkpoint_name
    })
    headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()


def genImage(prompt= "", width_image=512, height_image=512):
    url = "http://models_service:8081/gen_image/"

    payload = json.dumps({
    "prompt": prompt,
    "width_image": width_image,
    "height_image": height_image
    })
    headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response = response.json()

    return response
