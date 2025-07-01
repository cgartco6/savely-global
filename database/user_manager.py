from database.firebase_connector import db
import random
import string

def create_user(email, country):
    user_ref = db.collection('users')
    user_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    user_ref.document(user_id).set({
        'email': email,
        'country': country,
        'points': 100,  # Starting points
        'is_premium': False,
        'ad_views_today': 0
    })
    return user_id

def get_user(user_id):
    user_ref = db.collection('users').document(user_id)
    return user_ref.get().to_dict()

def update_points(user_id, points):
    user_ref = db.collection('users').document(user_id)
    user_ref.update({
        'points': firestore.Increment(points)
    })

def record_ad_view(user_id):
    user_ref = db.collection('users').document(user_id)
    user_ref.update({
        'ad_views_today': firestore.Increment(1)
    })
    
    # Check if reached 4 ads
    user = get_user(user_id)
    if user['ad_views_today'] >= 4:
        # Reset and reward
        user_ref.update({'ad_views_today': 0})
        reward_user(user_id)

def reward_user(user_id):
    # Give 100 points or other reward
    update_points(user_id, 100)

def upgrade_user(user_id):
    user_ref = db.collection('users').document(user_id)
    user_ref.update({
        'is_premium': True
    })
