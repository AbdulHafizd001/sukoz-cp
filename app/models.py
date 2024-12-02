import firebase_admin
from firebase_admin import credentials, firestore

# Inisialisasi Firebase Admin SDK
cred = credentials.Certificate("C:\\msib-abdul\\backend\\credentials.json")
firebase_admin.initialize_app(cred)

# Inisialisasi Firestore
db = firestore.client()

# Fungsi model untuk User
def add_user(user_data):
    db.collection('users').add(user_data)

def get_user(user_id):
    return db.collection('users').document(user_id).get().to_dict()

def update_user(user_id, user_data):
    db.collection('users').document(user_id).update(user_data)

def delete_user(user_id):
    db.collection('users').document(user_id).delete()
# --- USERS ---
def add_user(email, username, edge, birthday):
    user_ref = db.collection('users').document()
    user_ref.set({
        'email': email,
        'username': username,
        'edge': edge,  # Misalnya ini adalah usia atau informasi tambahan lainnya
        'birthday': birthday
    })
    return user_ref.id  # Mengembalikan ID pengguna yang baru ditambahkan

# Mengambil data pengguna berdasarkan ID
def get_user(user_id):
    user_ref = db.collection('users').document(user_id)
    user = user_ref.get()
    if user.exists:
        return user.to_dict()
    else:
        return None

# Mengupdate informasi pengguna
def update_user(user_id, email=None, username=None, edge=None, birthday=None):
    user_ref = db.collection('users').document(user_id)
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
    user_ref = db.collection('users').document(user_id)
    user_ref.delete()

# --- RECIPES ---
def add_recipe(name, category, ingredients, instructions, image_url):
    recipe_data = {
        "name": name,
        "category": category,
        "ingredients": ingredients,
        "instructions": instructions,
        "image_url": image_url
    }
    recipe_ref = db.collection('recipes').document()
    recipe_ref.set(recipe_data)
    return recipe_data

def get_recipe(recipe_id):
    return db.collection('recipes').document(recipe_id).get().to_dict()

def update_recipe(recipe_id, data):
    db.collection('recipes').document(recipe_id).update(data)

def delete_recipe(recipe_id):
    db.collection('recipes').document(recipe_id).delete()

# --- CATEGORIES ---
def add_category(name):
    category_ref = db.collection('categories').add({
        'name': name
    })
    return category_ref.id  # Mengembalikan ID kategori yang baru ditambahkan

def update_category(category_id, data):
    category_ref = db.collection('categories').document(category_id)
    if not category_ref.get().exists:
        return None
    category_ref.update({
        'name': data.get('name', '')
    })
    return category_ref.get().to_dict()  # Mengembalikan data kategori yang diperbarui

def get_category(category_id):
    category_ref = db.collection('categories').document(category_id)
    category = category_ref.get()
    if category.exists:
        return category.to_dict()
    else:
        return None

def delete_category(category_id):
    category_ref = db.collection('categories').document(category_id)
    if not category_ref.get().exists:
        return None
    category_ref.delete()
    return True

# --- RATINGS --- #baru aja mengubah get_ratings menjadi get_rating
def get_rating(filter_criteria):
    # Logika untuk mendapatkan daftar rating berdasarkan filter
    ratings = db.collection('ratings').where(filter_criteria['field'], '==', filter_criteria['value']).stream()
    return [rating.to_dict() for rating in ratings]
    
def add_rating(rating_id, user_id, recipe_id, score, comment):
    rating_ref = db.collection('ratings').document(rating_id)
    rating_ref.set({
        "user_id": user_id,
        "recipe_id": recipe_id,
        "score": score,
        "comment": comment
    })

def get_rating(rating_id):
    return db.collection('ratings').document(rating_id).get().to_dict()

def update_rating(rating_id, data):
    db.collection('ratings').document(rating_id).update(data)

def delete_rating(rating_id):
    db.collection('ratings').document(rating_id).delete()


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

