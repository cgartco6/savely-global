import requests
import os
from config.api_keys import TIKTOK_API_KEY, INSTAGRAM_API_KEY, FACEBOOK_API_KEY
import time

def post_to_all_platforms(recipe, video_path):
    print(f"📱 Posting {recipe['title']} to social platforms")
    
    platforms = [
        ("TikTok", post_to_tiktok),
        ("Instagram", post_to_instagram),
        ("Facebook", post_to_facebook)
    ]
    
    for platform_name, post_func in platforms:
        try:
            success = post_func(recipe, video_path)
            status = "✅" if success else "❌"
            print(f"{status} {platform_name}")
            time.sleep(2)  # Avoid rate limits
        except Exception as e:
            print(f"⚠️ Error posting to {platform_name}: {str(e)}")

def post_to_tiktok(recipe, video_path):
    caption = f"✨ New Fusion Recipe: {recipe['title']} ✨\n"
    caption += f"Combining {recipe['country']} cuisine with South African {recipe['sa_flavor']}\n"
    caption += "#FoodFusion #GlobalCuisine #RecipeIdeas"
    
    url = "https://open.tiktokapis.com/v2/post/publish/inbox/"
    headers = {"Authorization": f"Bearer {TIKTOK_API_KEY}"}
    
    with open(video_path, "rb") as video_file:
        files = {"video": video_file}
        data = {"caption": caption}
        response = requests.post(url, headers=headers, files=files, data=data)
    
    return response.status_code == 200

def post_to_instagram(recipe, video_path):
    # Instagram requires different approach - using Facebook Graph API
    page_id = "YOUR_INSTAGRAM_BUSINESS_ACCOUNT_ID"
    url = f"https://graph.facebook.com/v18.0/{page_id}/media"
    
    caption = f"✨ New Fusion Recipe: {recipe['title']} ✨\n\n"
    caption += f"Experience the unique blend of {recipe['country']} flavors with "
    caption += f"South African {recipe['sa_flavor']}\n\n"
    caption += "Full recipe at savelyglobal.com\n"
    caption += "#FoodInnovation #CulturalCuisine #RecipeInspiration"
    
    payload = {
        "caption": caption,
        "media_type": "REELS",
        "access_token": INSTAGRAM_API_KEY
    }
    
    with open(video_path, "rb") as video_file:
        files = {"video": video_file}
        response = requests.post(url, data=payload, files=files)
    
    if response.status_code == 200:
        creation_id = response.json()["id"]
        return publish_instagram_reel(creation_id)
    return False

def publish_instagram_reel(creation_id):
    url = f"https://graph.facebook.com/v18.0/{creation_id}/publish"
    params = {"access_token": INSTAGRAM_API_KEY}
    response = requests.post(url, params=params)
    return response.status_code == 200

def post_to_facebook(recipe, video_path):
    page_id = "YOUR_FACEBOOK_PAGE_ID"
    url = f"https://graph.facebook.com/v18.0/{page_id}/videos"
    
    caption = f"New Fusion Recipe: {recipe['title']}\n\n"
    caption += f"Blending {recipe['country']} culinary traditions with "
    caption += f"South African {recipe['sa_flavor']}\n\n"
    caption += "Full recipe: savelyglobal.com\n"
    caption += "#FoodCulture #FusionCuisine #CookingInspiration"
    
    params = {
        "description": caption,
        "access_token": FACEBOOK_API_KEY
    }
    
    with open(video_path, "rb") as video_file:
        files = {"source": video_file}
        response = requests.post(url, params=params, files=files)
    
    return response.status_code == 200
