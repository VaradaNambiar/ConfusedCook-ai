from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cook import llm_chef


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# To Import notebook functions here, the options are: 
# 1. Convert your notebook to .py file and import (selected)
# 2. Use nbconvert to import notebook functions
# 3. Copy your main function from the notebook

def process_ingredients(ingredients_text):

    food = llm_chef(ingredients_text)
    ingredients = [ing.strip() for ing in ingredients_text.split(',')]
    return {
        "recipe": {
            "title": f"AI-Generated Recipe with {', '.join(ingredients[:2])}",
            "description": f"A delicious recipe created using: {ingredients_text}",
            "ingredients": [f"{ing}" for ing in ingredients],
            "instructions": food,
        }
    }

@app.route('/')
def serve_ui():
    """Serve the main HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS)"""
    return send_from_directory('.', filename)

@app.route('/api/recipes', methods=['POST'])
def generate_recipe():
    """API endpoint for recipe generation"""
    try:
        data = request.get_json()
        
        if not data or 'ingredients' not in data:
            return jsonify({'error': 'Missing ingredients'}), 400
        
        ingredients = data['ingredients'].strip()
        
        if not ingredients:
            return jsonify({'error': 'Ingredients cannot be empty'}), 400
        
        result = process_ingredients(ingredients)
        return jsonify(result)
    
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    print("Starting ConfusedCook AI server...")
    print("UI available at: http://localhost:5000")
    print("API endpoint: http://localhost:5000/api/recipes")
    app.run(debug=True, host='0.0.0.0', port=5000)
