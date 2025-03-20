import json
import torch
import clip
import time
from PIL import Image
import numpy as np
import os

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-L/14", device=device)

# Charger les œuvres
with open("oeuvres.json", "r", encoding="utf-8") as f:
    oeuvres = json.load(f)

# Charger et prétraiter les images
image_dict = {}
for oeuvre in oeuvres:
    img_path = oeuvre["path"]
    try:
        image = preprocess(Image.open(img_path)).unsqueeze(0).to(device)
        image_dict[oeuvre["id_oeu"]] = image
    except Exception as e:
        print(f"Erreur lors du chargement de l'image {img_path}: {e}")

with torch.no_grad():
    image_features_dict = {k: model.encode_image(v) for k, v in image_dict.items()}

for k in image_features_dict:
    image_features_dict[k] /= image_features_dict[k].norm(dim=-1, keepdim=True)

def calculer_similarites(id_oeuvre, seuil=0.65):
    """ Calcule les similarités d'une œuvre avec les autres """
    if id_oeuvre not in image_features_dict:
        print(f"Oeuvre {id_oeuvre} non trouvée.")
        return {}
    
    selected_feature = image_features_dict[id_oeuvre]
    similarities = {}
    
    for k, v in image_features_dict.items():
        if k != id_oeuvre:
            similarity = (selected_feature @ v.T).cpu().numpy()[0][0]
            if similarity > seuil:
                similarities[k] = float(similarity)  # Conversion pour JSON
    
    return dict(sorted(similarities.items(), key=lambda x: x[1], reverse=True))

def charger_fichier_json(nom_fichier):
    """ Charge un fichier JSON en mémoire """
    if os.path.exists(nom_fichier):
        with open(nom_fichier, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print(f"Erreur de lecture du fichier {nom_fichier}")
                return []
    return []

def surveiller_likes():
    """ Surveille en continu le fichier like.json et met à jour les suggestions """
    dernier_id_oeu = None
    dernier_id_am = None

    while True:
        likes = charger_fichier_json("like.json")
        
        if not likes:
            time.sleep(2)  
            continue

        dernier_like = likes[-1]
        id_oeuvre_like = str(dernier_like["id_oeu"])
        id_am = dernier_like["id_am"]

        if id_oeuvre_like != dernier_id_oeu or id_am != dernier_id_am:
            print(f"Nouveau like détecté : {id_oeuvre_like} (id_am: {id_am})")

            resultats = calculer_similarites(id_oeuvre_like)
            
            suggestions = charger_fichier_json("suggest.json")
            
            utilisateur_existe = any(s["id_am"] == id_am for s in suggestions)
            
            if utilisateur_existe:
                for s in suggestions:
                    if s["id_am"] == id_am:
                        s["suggestions"].extend([{"id_oeu": k, "score": v} for k, v in resultats.items()])
                        s["suggestions"] = list({d["id_oeu"]: d for d in s["suggestions"]}.values())  
            else:
                suggestions.append({
                    "id_am": id_am,
                    "suggestions": [{"id_oeu": k, "score": v} for k, v in resultats.items()]
                })

            with open("suggest.json", "w", encoding="utf-8") as f:
                json.dump(suggestions, f, indent=4, ensure_ascii=False)
            
            dernier_id_oeu = id_oeuvre_like
            dernier_id_am = id_am

        time.sleep(2) 

surveiller_likes()
