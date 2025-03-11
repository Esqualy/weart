import torch
import clip
from PIL import Image
import numpy as np
import os
import datetime
import platform

# Charger CLIP et le modèle pré-entraîné
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-L/14", device=device)

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

# Interpréter les résultats
images_labels = [
    "Les Demoiselles d’Avignon - Picasso",
    "Guernica - Picasso",
    "La Nuit étoilée - van Gogh",
    "Le Baiser - Klimt",
    "La Persistance de la mémoire - Dali",
    "La Joconde - De Vinci"
]

# Paramétrage de l'anti-leak et configuration
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
config = {
    "thresholds": {
        "very_similar": 0.75,
        "quite_similar": 0.65,
        "somewhat_similar": 0.55
    },
    "device": device,
    "model": "ViT-L/14",
    "timestamp": timestamp,
    "note": "Accès restreint.",
}

# Récupérer des infos sur le système
os_info = platform.system()
cpu_info = platform.processor()
gpu_info = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "Aucun GPU détecté"

# Dossier pour le dump (créé s'il n'existe pas)
dump_dir = "weart_dumps"
if not os.path.exists(dump_dir):
    os.makedirs(dump_dir)

# Calcul du numéro du dump en fonction du nombre de fichiers existants
existing_files = [f for f in os.listdir(dump_dir) if f.startswith("weart_dump_") and f.endswith(".log")]
dump_count = len(existing_files) + 1  # Incrémentation du compteur

# Fichier de dump (avec extension .log)
dump_file = os.path.join(dump_dir, f"weart_dump_{dump_count}.log")

# Liste pour stocker les résultats
dump_results = []

# Ajouter les détails de configuration et de sécurité
dump_results.append(f"--- WeArt - Dump #{dump_count} ---\n")
dump_results.append(f"Timestamp: {timestamp}\n")
dump_results.append(f"Configuration utilisée:\n")
dump_results.append(f"Système d'exploitation: {os_info}\n")
dump_results.append(f"CPU: {cpu_info}\n")
dump_results.append(f"GPU: {gpu_info}\n")
dump_results.append(f"Seuils de similarité: {config['thresholds']}\n")
dump_results.append(f"Modèle utilisé: {config['model']}\n")
dump_results.append(f"Device: {config['device']}\n")
dump_results.append(f"Note: {config['note']}\n")

# Ajouter la liste des œuvres testées
dump_results.append(f"\nŒuvres testées :\n")
for label in images_labels:
    dump_results.append(f"- {label}\n")

dump_results.append("\n")

# Afficher les similarités et interpréter avec des seuils ajustés
for i in range(len(image_paths)):
    for j in range(i+1, len(image_paths)):
        similarity = similarity_matrix.cpu().numpy()[i][j]
        
        # Ajouter les résultats de la similarité
        dump_results.append(f"\nSimilarité entre {images_labels[i]} et {images_labels[j]} : {similarity:.4f}\n")
        print(f"Similarité entre {images_labels[i]} et {images_labels[j]} : {similarity:.4f}")
        
        # Interprétation des résultats avec des seuils ajustés
        if similarity > config["thresholds"]["very_similar"]:
            dump_results.append("Ces œuvres sont très similaires !\n")
            print("Ces œuvres sont très similaires !")
        elif similarity > config["thresholds"]["quite_similar"]:
            dump_results.append("Ces œuvres sont assez similaires.\n")
            print("Ces œuvres sont assez similaires.")
        elif similarity > config["thresholds"]["somewhat_similar"]:
            dump_results.append("Il y a une certaine ressemblance, mais elles sont différentes.\n")
            print("Il y a une certaine ressemblance, mais elles sont différentes.")
        else:
            dump_results.append("Ces œuvres sont peu similaires.\n")
            print("Ces œuvres sont peu similaires.")

# Ajouter la matrice de similarité
dump_results.append("\nMatrice des similarités entre images :\n")
similarity_matrix_str = str(similarity_matrix.cpu().numpy())
dump_results.append(similarity_matrix_str)
print("\nMatrice des similarités entre images :")
print(similarity_matrix_str)

# Sauvegarder les résultats dans le fichier de dump avec encodage utf-8
with open(dump_file, "w", encoding="utf-8") as f:
    f.writelines(dump_results)

print(f"\nLes résultats ont été sauvegardés dans : {dump_file}")
