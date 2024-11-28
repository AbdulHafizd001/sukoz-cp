import firebase_admin
from firebase_admin import credentials, firestore

# Inisialisasi Firestore
cred = credentials.Certificate('C:\\msib-abdul\\backend\\database_firestore\\credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def save_user(user_data):
    user_ref = db.collection('users').document(user_data['email'])
    user_ref.set({
        'username': user_data['username'],
        'age': user_data['age'],
        'birthday': user_data['birthday'],
        'verified': True
    })
