import random
from database.user_manager import record_ad_view, update_points

# Mock luxury ad inventory
LUXURY_ADS = [
    {"brand": "Rolex", "image": "rolex.jpg", "url": "https://rolex.com"},
    {"brand": "Tesla", "image": "tesla.jpg", "url": "https://tesla.com"},
    {"brand": "Louis Vuitton", "image": "lv.jpg", "url": "https://lv.com"},
    {"brand": "Emirates", "image": "emirates.jpg", "url": "https://emirates.com"}
]

def serve_ad(user_id):
    # Record view
    record_ad_view(user_id)
    
    # Select random ad
    ad = random.choice(LUXURY_ADS)
    
    # Add user-specific tracking
    ad['tracking_url'] = f"https://tracking.com?user={user_id}&ad={ad['brand']}"
    
    return ad
