import tweepy
import requests
import schedule
import time
from config.api_keys import (
    TIKTOK_API_KEY,
    INSTAGRAM_API_KEY,
    FACEBOOK_API_KEY
)

def post_to_tiktok(video_path, caption):
    # TikTok API integration
    url = "https://open.tiktokapis.com/v2/post/publish/"
    headers = {"Authorization": f"Bearer {TIKTOK_API_KEY}"}
    
    with open(video_path, "rb") as f:
        files = {"video": f}
        data = {"caption": caption}
        response = requests.post(url, headers=headers, files=files, data=data)
    
    return response.status_code == 200

def post_to_instagram(video_path, caption):
    # Instagram Basic Display API
    auth = tweepy.OAuthHandler(INSTAGRAM_API_KEY['consumer_key'], 
                              INSTAGRAM_API_KEY['consumer_secret'])
    auth.set_access_token(INSTAGRAM_API_KEY['access_token'], 
                         INSTAGRAM_API_KEY['access_token_secret'])
    api = tweepy.API(auth)
    
    media = api.media_upload(video_path)
    api.update_status(status=caption, media_ids=[media.media_id])
    return True

def post_to_facebook(video_path, caption):
    # Facebook Graph API
    url = f"https://graph.facebook.com/v18.0/me/videos"
    params = {
        "access_token": FACEBOOK_API_KEY,
        "caption": caption
    }
    
    with open(video_path, "rb") as f:
        files = {"source": f}
        response = requests.post(url, params=params, files=files)
    
    return response.status_code == 200

def schedule_posts():
    # Schedule daily posting
    schedule.every().day.at("09:00").do(post_all)
    while True:
        schedule.run_pending()
        time.sleep(60)

def post_all():
    # Get latest content from outputs
    latest_video = "outputs/videos/latest.mp4"
    caption = "Check out our new fusion recipe!"
    
    post_to_tiktok(latest_video, caption)
    post_to_instagram(latest_video, caption)
    post_to_facebook(latest_video, caption)
