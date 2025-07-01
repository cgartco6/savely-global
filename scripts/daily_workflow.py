from ai_agents.recipe_generator import generate_recipe
from ai_agents.image_creator import generate_food_image
from ai_agents.video_maker import create_short_video
from ai_agents.social_manager import post_all
from database.user_manager import save_recipe
from config.country_settings import COUNTRIES
import random

def daily_content_creation():
    # Generate recipes for 3 random countries
    for _ in range(3):
        country = random.choice(COUNTRIES)
        sa_flavor = random.choice(['rooibos', 'amarula', 'biltong', 'melktert'])
        
        recipe = generate_recipe(country, sa_flavor)
        image_path = generate_food_image(recipe['title'])
        caption = generate_social_caption(recipe)
        video_path = create_short_video(image_path, caption[:100])
        
        recipe_data = {
            **recipe,
            'image_path': image_path,
            'video_path': video_path,
            'caption': caption,
            'country': country
        }
        
        save_recipe(recipe_data)
    
    # Post to social media
    post_all()

if __name__ == '__main__':
    daily_content_creation()
