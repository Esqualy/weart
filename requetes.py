import json


def like(IdAm, IdOeu):
    """
    Système de like qui prends en entrée l'amateur et l'oeuvre qu'il a liké, pour créer une nouvelle ligne dans "amateur_oeuvre.json"
    si elle n'existe pas déjà.)
    """
    d={"IdAm":IdAm,"IdOeu":IdOeu}
    with open("amateur_oeuvre.json","r") as f:
        data = json.load(f)
        if d not in data:
            data.append(d)
    with open("amateur_oeuvre.json","w") as f:
        json.dump(data,f)
    print("données update")


def like_amateur (IdAm):
    """Prends en entrée l'id de l'amateur et renvoie les id des oeuvres qu'il a liké."""

    res = []
    with open("amateur_oeuvre.json","r") as f:
        data = json.load(f)
        for d in data:
            if d["IdAm"] == IdAm:
                res.append(d["IdOeu"])


def auteur(IdOeu):
    """Prends en entrée l'id d'une oeuvre et renvoie l'id de son artiste."""
    with open("oeuvres.json","r") as f:
        data = json.load(f)
        for d in data:
            if d["IdOeu"] == str(IdOeu):
                return d["IdAr"]
    return None


def oeuvres_auteur(IdAr):
    """Prends en entrée l'id  d'un artiste, et renvoie les ids des oeuvres qu'il a créées."""
    with open("oeuvres.json", "r") as f:
        data = json.load(f)
        IdAr = str(IdAr)
    return [d["IdOeu"] for d in data if d["IdAr"] == IdAr]


def oeuvres_auteurs(artists):
    """Prend en entrée une liste d'id d'artiste, renvoie la liste des id des oeuvres de ces artistes
    """
    res = []
    for x in artists:
        res.extend(oeuvres_auteur(x))
    return res


def like_oeuvre(IdOeu):
    with open("amateur_oeuvre.json", "r") as f:
        data = json.load(f)
        amateurs_likes = []
        for d in data:
            if d["IdOeu"] == IdOeu:
                amateurs_likes.append(d["IdAm"])
        if amateurs_likes:
            return amateurs_likes
        else:
            return "Aucun amateur n'a aimé cette œuvre"
      
        



def oeuvres_likées_amateur(IdAm):
    """Prends en entrée l'id d'un amateur, regarde les amateurs ayant liké les mêmes œuvres que lui, et renvoie leurs œuvres likées."""
    oeuvres_likées = like_amateur(IdAm)
    amateurs_ayant_les_mêmes_oeuvres = []
    with open("amateur_oeuvre.json", "r") as f:
        data = json.load(f)
        for d in data:
            if d["IdOeu"] in oeuvres_likées and d["IdAm"] != IdAm:
                amateurs_ayant_les_mêmes_oeuvres.append(d["IdAm"])

    # Récupérer toutes les œuvres likées par ces autres amateurs
    oeuvres_likées_par_autres_amateurs = oeuvres_auteurs(list(amateurs_ayant_les_mêmes_oeuvres))
    return ("IdOeu")

print(oeuvres_likées_amateur(1))