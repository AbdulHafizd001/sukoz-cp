from flask import Blueprint, request, jsonify
from app.models import add_recipe, get_recipe, update_recipe, delete_recipe

# Definisikan Blueprint dengan nama 'recipe_bp'
recipe_bp = Blueprint('recipe', __name__)

# Rute untuk membuat resep baru
@recipe_bp.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()
    name = data.get('name')
    category = data.get('category')
    ingredients = data.get('ingredients')
    instructions = data.get('instructions')
    image_url = data.get('image_url')

    if not all([name, category, ingredients, instructions, image_url]):
        return jsonify({"error": "All fields are required"}), 400

    new_recipe = add_recipe(name, category, ingredients, instructions, image_url)
    return jsonify({"message": "Recipe added successfully", "recipe": new_recipe}), 201


# Rute untuk mendapatkan resep berdasarkan ID
@recipe_bp.route('/recipes/<recipe_id>', methods=['GET'])
def get_recipe_by_id(recipe_id):
    recipe = get_recipe(recipe_id)
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404
    return jsonify({"recipe": recipe}), 200

@recipe_bp.route('/recipes/<recipe_id>', methods=['PUT'])
def modify_recipe(recipe_id):
    data = request.json
    update_recipe(recipe_id, data)
    return jsonify({"message": "Recipe updated successfully!"}), 200

@recipe_bp.route('/recipes/<recipe_id>', methods=['DELETE'])
def remove_recipe(recipe_id):
    delete_recipe(recipe_id)
    return jsonify({"message": "Recipe deleted successfully!"}), 200

