import requests
import os
from config.api_keys import HUGGINGFACE_API_KEY

def generate_food_image(prompt):
    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    
    payload = {
        "inputs": f"professional food photography, 8K, high detail: {prompt}",
        "options": {"wait_for_model": True}
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        output_path = f"outputs/images/{prompt[:20]}.jpg"
        with open(output_path, "wb") as f:
            f.write(response.content)
        return output_path
    else:
        print(f"Image generation failed: {response.text}")
        return None
