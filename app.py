import torch
import clip
from PIL import Image
import numpy as np

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-L/14", device=device)

image_paths = [
    "oeuvre1.jpg",
    "oeuvre2.jpg",
    "oeuvre3.jpg",
    "oeuvre4.jpg",
    "oeuvre5.jpg",
    "oeuvre6.jpg"
]

images = [preprocess(Image.open(img)).unsqueeze(0).to(device) for img in image_paths]

with torch.no_grad():
    image_features = torch.cat([model.encode_image(img) for img in images])

image_features /= image_features.norm(dim=-1, keepdim=True)

similarity_matrix = image_features @ image_features.T

print("Matrice des similarités entre images :")
similarity_matrix_np = similarity_matrix.cpu().numpy()
print(similarity_matrix_np)

images_labels = [
    "Les Tournesols - Van Gogh",
    "La Nuit étoilée - Van Gogh",
    "Impression, soleil levant - Monet",
    "Les Demoiselles d’Avignon - Picasso",
    "La Persistance de la mémoire - Dalí",
    "Composition VIII - Kandinsky"
]

for i in range(len(image_paths)):
    for j in range(i+1, len(image_paths)):
        similarity = similarity_matrix_np[i][j]
        print(f"\nSimilarité entre {images_labels[i]} et {images_labels[j]} : {similarity:.4f}")
        
        if similarity > 0.75:
            print("Ces œuvres sont très similaires !")
        elif similarity > 0.65:
            print("Ces œuvres sont assez similaires.")
        elif similarity > 0.55:
            print("Il y a une certaine ressemblance, mais elles sont différentes.")
        else:
            print("Ces œuvres sont peu similaires.")
