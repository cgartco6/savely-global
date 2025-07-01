import firebase_admin
from firebase_admin import credentials, firestore
from config.api_keys import FIREBASE_CONFIG

def init_firebase():
    cred = credentials.Certificate(FIREBASE_CONFIG)
    firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_firebase()

def save_recipe(recipe_data):
    recipes_ref = db.collection('recipes')
    recipes_ref.add(recipe_data)

def get_recipe(recipe_id):
    recipe_ref = db.collection('recipes').document(recipe_id)
    return recipe_ref.get().to_dict()

def get_free_recipes(limit=10):
    recipes_ref = db.collection('recipes').where('is_premium', '==', False).limit(limit)
    return [doc.to_dict() for doc in recipes_ref.stream()]

def get_premium_recipes(limit=10):
    recipes_ref = db.collection('recipes').where('is_premium', '==', True).limit(limit)
    return [doc.to_dict() for doc in recipes_ref.stream()]
