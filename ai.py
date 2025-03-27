import torch
import clip
from PIL import Image
import numpy as np

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-L/14", device=device)
#ViT-B/16
image_paths = [
    "oeuvre1.jpg",  # Chaise 1
    "oeuvre2.jpg",  # Chaise 2
    "oeuvre3.jpg",  # Table 1
    "oeuvre4.jpg",  # Table 2
    "oeuvre5.jpg",  # Avion 1
    "oeuvre6.jpg"   # Avion 2
]

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

images_labels = [
    "Chaise 1",
    "Chaise 2",
    "Table 1",
    "Table 2",
    "Avion 1",
    "Avion 2"
]

similar_images = {}

for i in range(len(image_paths)):
    res = []
    for j in range(i + 1, len(image_paths)):
        similarity = similarity_matrix_np[i][j]
        if similarity > 0.65: 
            res.append((images_labels[j], similarity))  
    similar_images[images_labels[i]] = res 
