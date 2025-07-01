import requests
import os
from config.api_keys import HUGGINGFACE_API_KEY
from PIL import Image
from io import BytesIO

def create_recipe_images(recipe_title, style="professional food photography"):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    
    prompt = f"{style} of {recipe_title}, 8K resolution, natural lighting, highly detailed, food magazine style"
    
    response = requests.post(
        API_URL, 
        headers=headers, 
        json={"inputs": prompt}
    )
    
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        filename = f"recipe_{recipe_title[:20].replace(' ', '_')}.jpg"
        save_path = os.path.join("outputs", "images", filename)
        image.save(save_path)
        return save_path
    else:
        print(f"⚠️ Image creation failed: {response.text}")
        return "default_recipe_image.jpg"
