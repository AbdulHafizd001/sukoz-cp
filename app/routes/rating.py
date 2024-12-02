from flask import Blueprint, request, jsonify
from app.models import db  # Impor langsung dari models.py
from app.models import add_rating, get_rating, delete_rating

rating_bp = Blueprint('rating', __name__)

# Add rating
@rating_bp.route('/ratings', methods=['POST'])
def create_rating():
    data = request.get_json()

    if not data or 'user_id' not in data or 'recipe_id' not in data or 'score' not in data:
        return jsonify({"error": "user_id, recipe_id, and score are required"}), 400

    try:
        rating_ref = db.collection('ratings').document()
        rating_ref.set({
            'user_id': data['user_id'],
            'recipe_id': data['recipe_id'],
            'score': data['score'],
            'comment': data.get('comment', '')  # comment optional
        })
        return jsonify({"message": "Rating added successfully", "rating_id": rating_ref.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Get rating by ID
@rating_bp.route('/ratings/<rating_id>', methods=['GET'])
def get_rating(rating_id):
    try:
        doc = db.collection('ratings').document(rating_id).get()

        if not doc.exists:
            return jsonify({"error": f"Rating with ID {rating_id} does not exist"}), 404

        return jsonify({
            "id": doc.id,
            **doc.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Update rating
@rating_bp.route('/ratings/<rating_id>', methods=['PUT'])
def update_rating(rating_id):
    data = request.get_json()

    if 'score' in data and not isinstance(data['score'], (int, float)):
        return jsonify({"error": "score must be a number"}), 400

    try:
        rating_ref = db.collection('ratings').document(rating_id)

        if not rating_ref.get().exists:
            return jsonify({"error": f"Rating with ID {rating_id} does not exist"}), 404

        rating_ref.update({
            'score': data.get('score', None),
            'comment': data.get('comment', '')
        })

        return jsonify({"message": f"Rating {rating_id} updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Delete rating
@rating_bp.route('/ratings/<rating_id>', methods=['DELETE'])
def delete_rating(rating_id):
    try:
        doc_ref = db.collection('ratings').document(rating_id)
        doc = doc_ref.get()

        if not doc.exists:
            return jsonify({"error": f"Rating with ID {rating_id} does not exist"}), 404

        doc_ref.delete()
        return jsonify({"message": f"Rating {rating_id} deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
