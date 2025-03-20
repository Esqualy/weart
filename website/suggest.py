import json
import torch
import clip
from PIL import Image
import numpy as np

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-L/14", device=device)

with open("oeuvres.json", "r", encoding="utf-8") as f:
    oeuvres = json.load(f)

with open("like.json", "r", encoding="utf-8") as f:
    likes = json.load(f)

# Charger et prétraiter les images
image_dict = {}
for oeuvre in oeuvres:
    img_path = oeuvre["path"]
    try:
        image = preprocess(Image.open(img_path)).unsqueeze(0).to(device)
        image_dict[oeuvre["IdOeu"]] = image
    except Exception as e:
        print(f"Erreur lors du chargement de l'image {img_path}: {e}")

with torch.no_grad():
    image_features_dict = {k: model.encode_image(v) for k, v in image_dict.items()}

for k in image_features_dict:
    image_features_dict[k] /= image_features_dict[k].norm(dim=-1, keepdim=True)

def calculer_similarites(IdOeu):
    if IdOeu not in image_features_dict:
        print("Oeuvre non trouvée dans les données.")
        return {}
    
    selected_feature = image_features_dict[IdOeu]
    similarities = {}
    
    for k, v in image_features_dict.items():
        if k != IdOeu:
            similarity = (selected_feature @ v.T).cpu().numpy()[0][0]
            similarities[k] = similarity
    
    return dict(sorted(similarities.items(), key=lambda x: x[1], reverse=True))

dernier_like = likes[-1]
IdOeu_like = str(dernier_like["IdOeu"])

resultats = calculer_similarites(IdOeu_like)

print(f"Matrice des similarités pour l'œuvre {IdOeu_like} :")
for IdOeu, score in resultats.items():
    print(f"{IdOeu}: {score:.4f}")
