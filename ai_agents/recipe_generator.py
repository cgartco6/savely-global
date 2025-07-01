import openai
import json
from config.api_keys import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_recipe(country, sa_flavor):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Create a fusion recipe combining {country} cuisine with South African {sa_flavor}:\n",
        max_tokens=500,
        temperature=0.7
    )
    
    recipe_text = response.choices[0].text.strip()
    
    # Parse into structured format
    sections = recipe_text.split("\n\n")
    return {
        "title": sections[0].replace("Recipe: ", ""),
        "description": sections[1],
        "ingredients": [i.strip() for i in sections[2].split("\n")[1:]],
        "instructions": [s.strip() for s in sections[3].split("\n")[1:]],
        "nutrition": sections[4] if len(sections) > 4 else ""
    }

def generate_social_caption(recipe):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Create engaging social media captions for this recipe: {recipe['title']}\n",
        max_tokens=120,
        temperature=0.8
    )
    return response.choices[0].text.strip()
