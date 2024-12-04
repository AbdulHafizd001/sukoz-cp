from flask import Blueprint, request, jsonify
from app.models import add_user, get_user, update_user, delete_user

# Definisikan blueprint dengan nama 'bp'
bp = Blueprint('user', __name__)

# Menambahkan pengguna baru
@bp.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    edge = data.get('edge')
    birthday = data.get('birthday')
    
    if not all([email, username, edge, birthday]):
        return jsonify({"error": "All fields are required"}), 400
    
    user_id = add_user(email, username, edge, birthday)
    return jsonify({"message": "User created", "user_id": user_id}), 201

# Mendapatkan data pengguna berdasarkan ID
@bp.route('/user/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user_data = get_user(user_id)
    if user_data:
        return jsonify(user_data), 200
    return jsonify({"error": "User not found"}), 404

# Mengupdate data pengguna
@bp.route('/user/<user_id>', methods=['PUT'])
def update_user_data(user_id):
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    edge = data.get('edge')
    birthday = data.get('birthday')

    update_user(user_id, email, username, edge, birthday)
    return jsonify({"message": "User updated"}), 200

# Menghapus pengguna berdasarkan ID
@bp.route('/user/<user_id>', methods=['DELETE'])
def delete_user_data(user_id):
    delete_user(user_id)
    return jsonify({"message": "User deleted"}), 200
