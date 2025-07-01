import requests
import os
import time
from config.api_keys import PIKA_API_KEY, ELEVENLABS_API_KEY

def create_recipe_videos(image_path, description):
    # Step 1: Create voiceover
    voiceover_path = create_voiceover(description)
    
    # Step 2: Create video with Pika
    video_path = create_pika_video(image_path, voiceover_path)
    
    return video_path

def create_voiceover(text):
    url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        filename = f"voiceover_{int(time.time())}.mp3"
        save_path = os.path.join("outputs", "audio", filename)
        with open(save_path, "wb") as f:
            f.write(response.content)
        return save_path
    else:
        print(f"⚠️ Voiceover creation failed: {response.text}")
        return None

def create_pika_video(image_path, audio_path):
    headers = {"Authorization": f"Bearer {PIKA_API_KEY}"}
    
    # Upload image
    with open(image_path, "rb") as img_file:
        img_response = requests.post(
            "https://api.pika.art/v1/upload", 
            headers=headers, 
            files={"file": img_file}
        )
    
    if img_response.status_code != 200:
        print("⚠️ Image upload failed")
        return None
        
    media_id = img_response.json()["mediaId"]
    
    # Create video
    video_data = {
        "mediaId": media_id,
        "text": "Savory Fusion Recipe",
        "audioUrl": audio_path,
        "duration": 15,
        "style": "cinematic"
    }
    
    video_response = requests.post(
        "https://api.pika.art/v1/create", 
        headers=headers, 
        json=video_data
    )
    
    if video_response.status_code != 200:
        print("⚠️ Video creation failed")
        return None
        
    video_id = video_response.json()["id"]
    
    # Wait for video processing
    for _ in range(10):
        status_response = requests.get(
            f"https://api.pika.art/v1/status/{video_id}", 
            headers=headers
        )
        status_data = status_response.json()
        
        if status_data["status"] == "completed":
            video_url = status_data["url"]
            return download_video(video_url)
            
        time.sleep(15)
        
    print("⚠️ Video processing timed out")
    return None

def download_video(url):
    response = requests.get(url)
    filename = f"recipe_video_{int(time.time())}.mp4"
    save_path = os.path.join("outputs", "videos", filename)
    
    with open(save_path, "wb") as f:
        f.write(response.content)
        
    return save_path
