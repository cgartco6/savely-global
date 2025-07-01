import openai
import json
from config.api_keys import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

SA_FLAVOR_PROFILES = {
    "rooibos": "caffeine-free herbal tea with earthy, sweet notes",
    "amarula": "creamy liqueur with caramel and tropical fruit flavors",
    "biltong": "dried, cured meat similar to jerky but less sweet",
    "melktert": "South African milk tart with cinnamon dusting"
}

def generate_daily_recipes(country, sa_flavor):
    # Get flavor profile
    flavor_profile = SA_FLAVOR_PROFILES.get(sa_flavor, "")
    
    # Create prompt
    prompt = f"""
    Create a novel fusion recipe that combines traditional {country} cuisine with 
    South African {sa_flavor} ({flavor_profile}). The recipe must:
    1. Be culturally respectful while innovative
    2. Include modern cooking techniques
    3. Feature at least one superfood ingredient
    4. Have a savory element
    5. Be structured with: Title, Description, Ingredients, Instructions, Nutrition
    
    Output in JSON format only with these keys:
    title, description, ingredients (list), instructions (list), nutrition
    """
    
    # Generate with OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a Michelin-star chef specializing in fusion cuisine"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=800
    )
    
    # Parse JSON response
    try:
        recipe = json.loads(response.choices[0].message.content)
        recipe['country'] = country
        recipe['sa_flavor'] = sa_flavor
        return recipe
    except json.JSONDecodeError:
        print("⚠️ Error parsing recipe JSON. Using fallback")
        return {
            "title": f"{country} - {sa_flavor} Fusion",
            "description": "Innovative cultural fusion recipe",
            "ingredients": [],
            "instructions": [],
            "nutrition": "",
            "country": country,
            "sa_flavor": sa_flavor
        }
