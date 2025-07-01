import random
from database.user_manager import record_ad_view, reward_user_for_ad
from config.api_keys import AD_SERVER_API_KEY

# Premium ad inventory (high CPM)
PREMIUM_ADS = [
    {
        "brand": "Le Creuset",
        "type": "banner",
        "image": "le_creuset.jpg",
        "url": "https://www.lecreuset.com",
        "cpm": 250  # $250 per 1000 views
    },
    {
        "brand": "Thermomix",
        "type": "video",
        "video": "thermomix_ad.mp4",
        "url": "https://thermomix.com",
        "cpm": 300
    },
    {
        "brand": "Emirates First Class",
        "type": "banner",
        "image": "emirates_first.jpg",
        "url": "https://www.emirates.com",
        "cpm": 400
    },
    {
        "brand": "Whole Foods Premium",
        "type": "video",
        "video": "whole_foods_ad.mp4",
        "url": "https://wholefoodsmarket.com",
        "cpm": 200
    }
]

def serve_ads():
    print("🪧 Serving premium ads to users")
    # This would integrate with your frontend to actually serve ads
    # Implementation depends on your web framework
    
def track_ad_performance():
    print("📊 Tracking ad performance")
    # This would collect analytics and report to ad partners
    
def get_ad_for_user(user_id):
    """Select and return an ad for a specific user"""
    ad = random.choice(PREMIUM_ADS)
    record_ad_view(user_id, ad['brand'], ad['cpm'])
    
    # Reward user for ad view
    reward_user_for_ad(user_id)
    
    return {
        "type": ad["type"],
        "content": ad["image"] if ad["type"] == "banner" else ad["video"],
        "url": ad["url"],
        "tracking_url": f"https://ads.savelyglobal.com/track?user={user_id}&ad={ad['brand']}"
    }
