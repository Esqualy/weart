import json
import torch
import clip
from PIL import Image
import numpy as np
from requetes import like_amateur 

SeuildeSimilarité = 0.65

def load_oeuvres(json_file='oeuvres.json'):
    """
    Charge oeuvres.json (pratique pour pas répéter ça tt le temps)
    """
    with open(json_file, 'r') as f:
        oeuvres = json.load(f)
    return oeuvres

def matrice_similarité(oeuvres, device=None, model_name="ViT-L/14"):
    """
    Lance la matrice de similarité et crée le classement entre les oeuvres
    sous forme de tableau NumPy, puis renvoie la liste des titres des oeuvres.
    """
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load(model_name, device=device)
    
    image_paths = [oeuvre["path"] for oeuvre in oeuvres]
    titres_oeuvre = [oeuvre["titre"] for oeuvre in oeuvres]
    
    images = []
    for img_path in image_paths:
        try:    
            image = Image.open(img_path)
        except Exception as e:
            print(f"Erreur lors de l'ouverture de {img_path}: {e}")
            continue
        images.append(preprocess(image).unsqueeze(0).to(device))
    
    with torch.no_grad():
        image_features = torch.cat([model.encode_image(img) for img in images])
    
    image_features /= image_features.norm(dim=-1, keepdim=True)

    similarity_matrix = image_features @ image_features.T
    similarity_matrix_np = similarity_matrix.cpu().numpy()
    
    return similarity_matrix_np, titres_oeuvre

def oeuvres_similaires(titres_oeuvres, similarity_matrix, s_similarité=SeuildeSimilarité):
    """
    Prends en entrée une oeuvre et renvoie toutes les oeuvres similaires
    dépassant le seuil de similarité de la matrice.
    """
    oeuvres_similaires = {}
    n = len(titres_oeuvres)
    for i in range(n):
        liste_similaire = []
        for j in range(n):
            if i != j:
                score = similarity_matrix[i][j]
                if score > s_similarité:
                    liste_similaire.append((titres_oeuvres[j], score))
        oeuvres_similaires[titres_oeuvres[i]] = liste_similaire
    return oeuvres_similaires