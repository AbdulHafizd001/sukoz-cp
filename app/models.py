import firebase_admin
from firebase_admin import credentials, firestore
from app.config import Config

# Inisialisasi Firebase Admin SDK
cred = credentials.Certificate(Config.FIREBASE_KEY_PATH)
firebase_admin.initialize_app(cred)

# Inisialisasi Firestore
db = firestore.client()

# Fungsi model untuk User
def add_user(user_data):
    db.collection('user').add(user_data)

def get_user(user_id):
    return db.collection('user').document(user_id).get().to_dict()

def update_user(user_id, user_data):
    db.collection('user').document(user_id).update(user_data)

def delete_user(user_id):
    db.collection('user').document(user_id).delete()
# --- USERS ---
def add_user(email, username, edge, birthday):
    user_ref = db.collection('user').document()
    user_ref.set({
        'email': email,
        'username': username,
        'edge': edge,  # Misalnya ini adalah usia atau informasi tambahan lainnya
        'birthday': birthday
    })
    return user_ref.id  # Mengembalikan ID pengguna yang baru ditambahkan

# Mengambil data pengguna berdasarkan ID
def get_user(user_id):
    user_ref = db.collection('user').document(user_id)
    user = user_ref.get()
    if user.exists:
        return user.to_dict()
    else:
        return None

# Mengupdate informasi pengguna
def update_user(user_id, email=None, username=None, edge=None, birthday=None):
    user_ref = db.collection('user').document(user_id)
    update_data = {}
    if email:
        update_data['email'] = email
    if username:
        update_data['username'] = username
    if edge:
        update_data['edge'] = edge
    if birthday:
        update_data['birthday'] = birthday
    user_ref.update(update_data)

# Menghapus pengguna berdasarkan ID
def delete_user(user_id):
    user_ref = db.collection('user').document(user_id)
    user_ref.delete()

# untuk login
def get_user_by_email(email):
    user = db.collection('user').where('email', '==', email).stream()
    for user in user:
        return user.to_dict()
    return None

# --- RECIPE ---
def add_recipe(name, category, ingredients, instructions, image_url):
    recipe_data = {
        "name": name,
        "category": category,
        "ingredients": ingredients,
        "instructions": instructions,
        "image_url": image_url
    }
    recipe_ref = db.collection('recipe').document()
    recipe_ref.set(recipe_data)
    return recipe_data

def get_recipe(recipe_id):
    return db.collection('recipe').document(recipe_id).get().to_dict()

def update_recipe(recipe_id, data):
    db.collection('recipe').document(recipe_id).update(data)

def delete_recipe(recipe_id):
    db.collection('recipe').document(recipe_id).delete()

# --- CATEGORIES ---
def add_category(name):
    category_ref = db.collection('category').add({
        'name': name
    })
    return category_ref.id  # Mengembalikan ID kategori yang baru ditambahkan

def update_category(category_id, data):
    category_ref = db.collection('category').document(category_id)
    if not category_ref.get().exists:
        return None
    category_ref.update({
        'name': data.get('name', '')
    })
    return category_ref.get().to_dict()  # Mengembalikan data kategori yang diperbarui

def get_category(category_id):
    category_ref = db.collection('category').document(category_id)
    category = category_ref.get()
    if category.exists:
        return category.to_dict()
    else:
        return None

def delete_category(category_id):
    category_ref = db.collection('category').document(category_id)
    if not category_ref.get().exists:
        return None
    category_ref.delete()
    return True

# --- BOOKMARKS ---
def add_bookmark(bookmark_id, user_id, recipe_id):
    bookmark_ref = db.collection('bookmark').document(bookmark_id)
    bookmark_ref.set({
        "user_id": user_id,
        "recipe_id": recipe_id,
    })

def get_bookmark(user_id):
    bookmark = db.collection('bookmark').where("user_id", "==", user_id).stream()
    return [{bookmark.id: bookmark.to_dict()} for bookmark in bookmark]

def delete_bookmark(bookmark_id):
    db.collection('bookmark').document(bookmark_id).delete()

