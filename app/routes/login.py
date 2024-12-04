from flask import Blueprint, request, jsonify
from app.models import get_user_by_email  # Pastikan fungsi ini ada di models.py

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = get_user_by_email(email)  # Fungsi ini akan mengambil data pengguna berdasarkan email
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user['password'] != password:  # Perbandingan langsung tanpa hash
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"message": "Login successful"}), 200
