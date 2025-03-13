import torch
import clip
from PIL import Image
import numpy as np
import random

########################VARIABLES########################

nbartists = 3
nboeuvres = 12
nbamateurs = 4

oeuvres_artist = {}
amateur_oeuvre = {}

###############DEFINITIONS DE FONCTIONS####################
def link_amateur_oeuvres():
    amateur_dict = {}
    for i in range(nbamateurs):
        amateur = f"amateur_{i+1}"  # On nomme les amateurs
        artiste_favori = random.randint(0, max(oeuvres_artists.values()))  # Choix d’un artiste favori
        oeuvres_de_l_artiste = [oeuvre for oeuvre, artiste in oeuvres_artists.items() if artiste == artiste_favori]
        nb_oeuvres = min(5, len(oeuvres_de_l_artiste))  # L'amateur peut aimer jusqu'à 5 œuvres
        oeuvres = random.sample(oeuvres_de_l_artiste, nb_oeuvres) if oeuvres_de_l_artiste else []
        amateur_dict[amateur] = {"artiste_favori": artiste_favori, "oeuvres_aimees": oeuvres}
    return amateur_dict

########################RECOMMANDATION PAR IA########################

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-L/14", device=device)

def recommander_oeuvres():
    recommendations = {}

########################ALGORITHME########################
amateur_oeuvre = link_amateur_oeuvres()
print(amateur_oeuvre)
