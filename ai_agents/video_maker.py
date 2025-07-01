import requests
import json
import time
from config.api_keys import PIKA_API_KEY

def create_short_video(image_path, caption):
    # Upload image to Pika
    upload_url = "https://api.pika.art/v1/upload"
    headers = {"Authorization": f"Bearer {PIKA_API_KEY}"}
    
    with open(image_path, "rb") as f:
        files = {"file": f}
        response = requests.post(upload_url, headers=headers, files=files)
    
    if response.status_code != 200:
        print("Image upload failed")
        return None
        
    media_id = response.json()["mediaId"]
    
    # Create video
    create_url = "https://api.pika.art/v1/create"
    payload = {
        "mediaId": media_id,
        "text": caption,
        "style": "cinematic",
        "duration": 15
    }
    
    response = requests.post(create_url, headers=headers, json=payload)
    video_id = response.json()["id"]
    
    # Check status
    status_url = f"https://api.pika.art/v1/status/{video_id}"
    for _ in range(10):  # Check every 10 seconds
        response = requests.get(status_url, headers=headers)
        status = response.json()["status"]
        if status == "completed":
            video_url = response.json()["url"]
            return download_video(video_url)
        time.sleep(10)
    
    return None

def download_video(url):
    response = requests.get(url)
    output_path = f"outputs/videos/video_{time.time()}.mp4"
    with open(output_path, "wb") as f:
        f.write(response.content)
    return output_path
