import torch
import clip
from PIL import Image
import numpy as np

# Charger CLIP et le modèle pré-entraîné
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-L/14", device=device)
#ViT-L/14 ; ViT-B/32	

# Liste des images (remplace par les chemins réels)
image_paths = [
    "oeuvre1.jpg",  # Les Tournesols - Van Gogh
    "oeuvre2.jpg",  # La Nuit étoilée - Van Gogh
    "oeuvre3.jpg",  # Impression, soleil levant - Monet
    "oeuvre4.jpg",  # Les Demoiselles d’Avignon - Picasso
    "oeuvre5.jpg",  # La Persistance de la mémoire - Dalí
    "oeuvre6.jpg"   # Composition VIII - Kandinsky
]

# Charger et prétraiter les images
images = [preprocess(Image.open(img)).unsqueeze(0).to(device) for img in image_paths]

# Extraire les embeddings
with torch.no_grad():
    image_features = torch.cat([model.encode_image(img) for img in images])

# Normaliser les embeddings
image_features /= image_features.norm(dim=-1, keepdim=True)

# Calculer la similarité cosinus entre les images
similarity_matrix = image_features @ image_features.T  # Produit scalaire des embeddings

# Afficher la matrice des similarités
print("Matrice des similarités entre images :")
similarity_matrix_np = similarity_matrix.cpu().numpy()
print(similarity_matrix_np)

# Interpréter les résultats
images_labels = [
    "Les Tournesols - Van Gogh",
    "La Nuit étoilée - Van Gogh",
    "Impression, soleil levant - Monet",
    "Les Demoiselles d’Avignon - Picasso",
    "La Persistance de la mémoire - Dalí",
    "Composition VIII - Kandinsky"
]

# Afficher les similarités et interpréter
for i in range(len(image_paths)):
    for j in range(i+1, len(image_paths)):
        similarity = similarity_matrix_np[i][j]
        print(f"\nSimilarité entre {images_labels[i]} et {images_labels[j]} : {similarity:.4f}")
        
        # Interprétation des résultats avec des seuils ajustés
        if similarity > 0.75:  # Plus élevé pour des œuvres vraiment similaires
            print("Ces œuvres sont très similaires !")
        elif similarity > 0.65:  # Ajustement du seuil pour des œuvres plus distinctes
            print("Ces œuvres sont assez similaires.")
        elif similarity > 0.55:  # Pour des œuvres moyennement similaires
            print("Il y a une certaine ressemblance, mais elles sont différentes.")
        else:
            print("Ces œuvres sont peu similaires.")
