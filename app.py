"""
ajouter une description du rôle de ce module dans le projet entier
ajouter une description succinte de son fonctionnement
Il me semble que tu fais essentiellement deux choses dans ce module : 
1. construire la matrice de similarités avec ton réseau de neurones ;
1. proposer un algorithme de suggestion basé sur cette matrice de similarités

Pour plus de clarté et de modularité, il me semble qu'il serait bon :
1. de mettre le traitement qui conduit à la matrice de similarité dans un fichier
1. Peut-être écrire la matrice de similarités dans un fichier à part
1. Enfin, dans un troisième fichier, rédiger sous forme d'une def l'algo de suggestions basé sur l'IA

Ainsi, si on imagine une interface admin qui permet d'ajouter une oeuvre. A part déposer le fichier image, on aura la mise à jour des json, et le recalcul de la matrice de similarité
Ensuite, la fonction suggestions pourra être appelée (à quel moment d'ailleurs ? et depuis quelle vue ?)
"""
import torch
import clip
from PIL import Image
import numpy as np
import json

# Charge le fichier JSON avec le reste
with open('oeuvres.json', 'r') as f:
    oeuvres = json.load(f)


device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-L/14", device=device)
#ViT-B/16

image_paths = [oeuvre["path"] for oeuvre in oeuvres]
image_labels = [oeuvre["titre"] for oeuvre in oeuvres]

# Charger et prétraiter les images
images = [preprocess(Image.open(img)).unsqueeze(0).to(device) for img in image_paths]

# Extraire les embeddings - representation vectorielle 
with torch.no_grad():
    image_features = torch.cat([model.encode_image(img) for img in images])

# Normaliser les embeddings
image_features /= image_features.norm(dim=-1, keepdim=True)

# Calculer la similarité cosinus entre les images
similarity_matrix = image_features @ image_features.T  # Produit scalaire des embeddings

print("Matrice des similarités entre images :")
similarity_matrix_np = similarity_matrix.cpu().numpy()
print(similarity_matrix_np)

similar_images = {}

for i in range(len(image_paths)):
    res = []
    for j in range(i + 1, len(image_paths)):
        similarity = similarity_matrix_np[i][j]
        if similarity > 0.65: 
            res.append((image_labels[j], similarity))  
    similar_images[image_labels[i]] = res 
