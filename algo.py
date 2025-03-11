'''
Les gars, prennez ce code en base, faites une copie et ajoutez des élémennts du code de Thibault dedans **IL FAUT QUE TOUT LE MONDE COMPRENNE TOUT LE CODE** et permettez vous d'y ajouter des trucs pertinnants
Boone nuit les guys

'''



import random

########################VARIABLES########################

nbartists = 4
nboeuvres = 56
nbamateurs = 12

oeuvres_artist = {}
amateur_oeuvre = {}

###############DEFINITIONS DE FONCTIONS####################
def link_oeuvres_artists():
    oeuvres_dict = {}
    for i in range(nboeuvres):
        artiste = random.randint(0, nbartists - 1)  # Choix d'un artiste aléatoire
        oeuvre_name = f"oeuvre_{i+1}"
        oeuvres_dict[oeuvre_name] = artiste
    return oeuvres_dict

def link_amateur_oeuvres():
    amateur_dict = {}
    for i in range(nbamateurs):
        amateur = f"amateur_{i+1}"
        oeuvre_aime = random.randint(1, nboeuvres // 3)
        oeuvres = random.sample(list(oeuvres_artist.keys()), nb_oeuvres)
        amateur_dict[amateur] = oeuvres
    return amateur_dict

########################ALGORITHME########################

oeuvres_artists = link_oeuvres_artists()
amateur_oeuvre = link_amateur_oeuvres()
print(oeuvres_artists)
print(amateur_oeuvre)
