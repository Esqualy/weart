import random

########################VARIABLES########################

nbartists = 4
nboeuvres = 56
nbamateurs = 12

oeuvres_artist = {}
amateur_oeuvre = {}

###############DEFINITIONS DE FONCTIONS####################
def link_oeuvres_artists() -> :
    oeuvres_dict = {}
    for i in range(nboeuvres):
        artiste = random.randint(0, nbartists - 1)  # On choisit un artiste au hasard
        oeuvre_name = f"oeuvre_{i+1}"  # Nom de l'œuvre
        oeuvres_dict[oeuvre_name] = artiste  # On associe l'œuvre à un artiste
    return oeuvres_dict

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

oeuvres_artists = link_oeuvres_artists()
amateur_oeuvre = link_amateur_oeuvres()
print(oeuvres_artists)
print(amateur_oeuvre)
