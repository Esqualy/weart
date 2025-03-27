def generate_unique_id(file_name, user_type):
    existing_ids = set()
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            users = json.load(f)
            for user in users:
                existing_ids.add(user.get(f"Id{user_type}", ""))  # Vérifie IdAm ou IdAr
    
    while True:
        new_id = str(random.randint(10**17, 10**18 - 1))
        if new_id not in existing_ids:
            return new_id

def save_user_to_json(user_type, pseudo, password, mail, ddn, nom, prenom, genre):
    file_name = f"{user_type}.json"
    user_id_key = "IdAr" if user_type == "artiste" else "IdAm"
    user_id = generate_unique_id(file_name, user_type)
    default_pp = "https://cdn.we-art.art/static/pp/default.jpg"
    
    user_data = {
        user_id_key: user_id,
        "pseudo": pseudo,
        "password": password,
        "mail": mail,
        "ddn": ddn,
        "nom": nom,
        "prenom": prenom,
        "genre": genre,
        "profile_picture": default_pp,
        "bio": None  
    }
    
    users = []
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            users = json.load(f)
    
    users.append(user_data)
    with open(file_name, 'w') as f:
        json.dump(users, f, indent=2)
