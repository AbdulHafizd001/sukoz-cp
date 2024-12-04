from flask import Blueprint, request, jsonify
from app.models import db, add_bookmark as add_bookmark_model, get_bookmark as get_bookmark_model, delete_bookmark as delete_bookmark_model

bookmark_bp = Blueprint('bookmark', __name__)

# Add bookmark
@bookmark_bp.route('/bookmark', methods=['POST'])
def create_bookmark(): 
    data = request.get_json()

    if not data or 'user_id' not in data or 'recipe_id' not in data:
        return jsonify({"error": "user_id and recipe_id are required"}), 400

    try:
        bookmark_id = db.collection('bookmark').document().id  # Generate ID secara otomatis
        add_bookmark_model(bookmark_id, data['user_id'], data['recipe_id'])
        return jsonify({"message": "Bookmark added successfully", "bookmark_id": bookmark_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update bookmark
@bookmark_bp.route('/bookmark/<bookmark_id>', methods=['PUT'])
def update_bookmark(bookmark_id):
    data = request.get_json()

    try:
        bookmark_ref = db.collection('bookmark').document(bookmark_id)

        if not bookmark_ref.get().exists:
            return jsonify({"error": f"Bookmark with ID {bookmark_id} does not exist"}), 404

        # Update data bookmark
        bookmark_ref.update({
            'user_id': data.get('user_id', ''),
            'recipe_id': data.get('recipe_id', '')
        })

        return jsonify({"message": f"Bookmark {bookmark_id} updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get bookmarks for user
@bookmark_bp.route('/bookmark/user/<user_id>', methods=['GET'])
def get_user_bookmark(user_id):
    try:
        bookmark = get_bookmark_model(user_id)
        return jsonify(bookmark), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get all bookmarks (Read All)
@bookmark_bp.route('/bookmark', methods=['GET'])
def get_all_bookmark():
    try:
        bookmark = db.collection('bookmark').stream()
        bookmark_list = [{bookmark.id: bookmark.to_dict()} for bookmark in bookmark]
        return jsonify(bookmark_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete bookmark
@bookmark_bp.route('/bookmark/<bookmark_id>', methods=['DELETE'])
def remove_bookmark(bookmark_id):
    try:
        doc_ref = db.collection('bookmark').document(bookmark_id)
        doc = doc_ref.get()

        if not doc.exists:
            return jsonify({"error": f"Bookmark with ID {bookmark_id} does not exist"}), 404

        delete_bookmark_model(bookmark_id)
        return jsonify({"message": f"Bookmark {bookmark_id} deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
