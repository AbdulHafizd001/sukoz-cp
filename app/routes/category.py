from flask import Blueprint, request, jsonify
from app.models import db  # Pastikan db diimpor dari models.py

category_bp = Blueprint('category', __name__)

# Create a new category
@category_bp.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({"error": "The 'name' is required"}), 400

    name = data['name']

    try:
        # Membuat dokumen baru dengan ID otomatis
        category_ref = db.collection('categories').document()  # Firestore akan menghasilkan ID otomatis
        category_ref.set({
            'name': name
        })

        # Mengembalikan respons dengan ID kategori yang baru
        return jsonify({
            "message": "Category added successfully",
            "category_id": category_ref.id  # Mengambil ID dokumen yang baru
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Delete category
@category_bp.route('/categories/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        # Referensi dokumen kategori
        category_ref = db.collection('categories').document(category_id)
        doc = category_ref.get()

        # Cek jika kategori tidak ada
        if not doc.exists:
            return jsonify({"error": f"Category with ID {category_id} does not exist"}), 404

        # Hapus kategori
        category_ref.delete()
        return jsonify({"message": f"Category {category_id} deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Update an existing category
@category_bp.route('/categories/<category_id>', methods=['PUT'])
def update_category(category_id):
    data = request.get_json()

    try:
        category_ref = db.collection('categories').document(category_id)

        # Cek apakah kategori ada di Firestore
        if not category_ref.get().exists:
            return jsonify({"error": f"Category with ID {category_id} does not exist"}), 404

        # Update kategori
        category_ref.update({
            'name': data.get('name', '')  # Jika nama baru diberikan, akan diperbarui
        })

        return jsonify({"message": f"Category {category_id} updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Get category by ID
@category_bp.route('/categories/<category_id>', methods=['GET'])
def get_category(category_id):
    try:
        doc = db.collection('categories').document(category_id).get()

        # Cek jika kategori tidak ada
        if not doc.exists:
            return jsonify({"error": f"Category with ID {category_id} does not exist"}), 404

        return jsonify({
            "id": doc.id,
            **doc.to_dict()  # Mengambil semua data kategori
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
