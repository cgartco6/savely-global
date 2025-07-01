from flask import Flask, render_template, request, jsonify, send_file
from database.user_manager import init_db
from ai_agents.ad_bot import get_ad_for_user
import os

app = Flask(__name__)

# Initialize database
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recipe/<int:recipe_id>')
def recipe_page(recipe_id):
    # Would fetch recipe from database
    recipe = {
        "title": "Sample Fusion Recipe",
        "description": "Delicious cultural fusion",
        "ingredients": ["Ingredient 1", "Ingredient 2"],
        "instructions": ["Step 1", "Step 2"]
    }
    return render_template('recipe.html', recipe=recipe)

@app.route('/premium')
def premium():
    return render_template('premium.html')

@app.route('/download/<int:recipe_id>')
def download_recipe(recipe_id):
    # Would generate PDF from recipe data
    return send_file('sample_recipe.pdf', as_attachment=True)

@app.route('/ad')
def serve_ad():
    user_id = request.args.get('user_id', 'default_user')
    ad = get_ad_for_user(user_id)
    return jsonify(ad)

@app.route('/purchase-premium', methods=['POST'])
def purchase_premium():
    # Process payment
    # Would integrate with Stripe/Coinbase
    return jsonify({"status": "success", "message": "Premium access granted"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
