from flask import Flask, render_template, send_file, request
import os
from database.user_manager import UserManager
from ai_agents.payment_handler import process_payment
from ai_agents.ad_bot import serve_ad
from database.user_manager import create_user

@app.route('/ad')
def serve_ad():
    user_id = request.args.get('user')
    if not user_id:
        return {"error": "User missing"}, 400
    
    ad = serve_ad(user_id)
    return jsonify(ad)

@app.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    return payment_handler.process_webhook(request)
app = Flask(__name__)
user_manager = UserManager()

@app.route('/')
def home():
    return render_template('index.html', 
                          recipes=user_manager.get_free_recipes())

@app.route('/recipe/<recipe_id>')
def recipe_page(recipe_id):
    recipe = user_manager.get_recipe(recipe_id)
    return render_template('recipe.html', recipe=recipe)

@app.route('/download/<recipe_id>')
def download_recipe(recipe_id):
    recipe = user_manager.get_recipe(recipe_id)
    return send_file(recipe['pdf_path'], as_attachment=True)

@app.route('/premium', methods=['GET', 'POST'])
def premium():
    if request.method == 'POST':
        country = request.form['country']
        currency = request.form['currency']
        if process_payment(country, currency):
            return render_template('premium.html', 
                                  success=True,
                                  recipes=user_manager.get_premium_recipes())
    return render_template('premium.html', countries=get_countries())

def get_countries():
    # Return supported countries
    return ['US', 'UK', 'DE', 'JP', 'ZA', 'AU', 'NZ']

if __name__ == '__main__':
    app.run(port=5000)
