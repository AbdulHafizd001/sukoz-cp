from flask import Flask, request, jsonify
from models.firestore import save_user
from services.otp_service import send_otp, verify_otp
from firebase_admin import firestore

app = Flask(__name__)

# Endpoint untuk registrasi
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    username = data.get('username')
    age = data.get('age')
    birthday = data.get('birthday')

    if not all([email, username, age, birthday]):
        return jsonify({'error': 'All fields are required'}), 400

    otp = send_otp(email)
    return jsonify({'message': 'OTP sent to email', 'otp': otp}), 200

# Endpoint untuk verifikasi OTP
@app.route('/verify-otp', methods=['POST'])
def verify():
    data = request.json
    email = data.get('email')
    otp = data.get('otp')

    if verify_otp(email, otp):
        save_user(data)  # Simpan data user ke Firestore
        return jsonify({'message': 'Email verified, registration successful'}), 200

    return jsonify({'error': 'Invalid OTP'}), 400

# Endpoint untuk Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')  # Jika menggunakan password

    # Validasi input
    if not email or not password:
        return jsonify({"message": "Email dan password harus diisi"}), 400

    # Cek data di Firestore
    db = firestore.client()
    user_ref = db.collection('users').document(email)
    user = user_ref.get()

    if not user.exists:
        return jsonify({"message": "Pengguna tidak ditemukan"}), 404

    user_data = user.to_dict()

    # Verifikasi password jika digunakan
    if user_data.get('password') != password:
        return jsonify({"message": "Password salah"}), 401

    # Jika login berhasil
    return jsonify({
        "message": "Login berhasil",
        "user": {
            "email": email,
            "username": user_data.get('username'),
            "age": user_data.get('age'),
            "birthday": user_data.get('birthday'),
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Pastikan hanya ada satu app.run() di sini
