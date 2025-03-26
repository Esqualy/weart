import json

def like(IdAm, IdOeu):
    """
    Ajoute un like d'un amateur pour une œuvre.
    """
    d = {"IdAm": IdAm, "IdOeu": IdOeu}
    with open("amateur_oeuvre.json", "r") as f:
        data = json.load(f)
    if d not in data:
        data.append(d)
        with open("amateur_oeuvre.json", "w") as f:
            json.dump(data, f)
    print("Données mises à jour")

def like_amateur(IdAm):
    """
    Renvoie la liste des ID d'œuvres likées par un amateur .
    """
    res = []
    with open("amateur_oeuvre.json", "r") as f:
        data = json.load(f)
    for d in data:
        if d["IdAm"] == IdAm:
            res.append(d["IdOeu"])
    return res

def like_amateurs(amateurs):
    """
    Renvoie la liste des ID d'œuvres likées par des amateurs.
    """
    res = []
    with open("amateur_oeuvre.json", "r") as f:
        data = json.load(f)
    for IdAm in amateurs:
        for d in data:
            if d["IdAm"] == IdAm:
                res.append(d["IdOeu"])
    return res

def auteur(IdOeu):
    """
    Renvoie l'ID de l'artiste ayant créé l'œuvre spécifiée.
    """
    with open("oeuvres.json", "r") as f:
        data = json.load(f)
    for d in data:
        if d["IdOeu"] == str(IdOeu):
            return d["IdAr"]
    return None

def oeuvres_auteur(IdAr):
    """
    Renvoie la liste des ID d'œuvres créées par un artiste donné.
    """
    with open("oeuvres.json", "r") as f:
        data = json.load(f)
    return [d["IdOeu"] for d in data if d["IdAr"] == str(IdAr)]

def oeuvres_auteurs(artists):
    """
    Renvoie une liste d'œuvres créées par une liste d'artistes.
    """
    res = []
    for x in artists:
        res.extend(oeuvres_auteur(x))
    return res

def like_oeuvres(oeuvres):
    """
    Renvoie la liste des amateurs ayant liké une des oeuvres de la liste prise en entrée.
    """
    with open("amateur_oeuvre.json", "r") as f:
        data = json.load(f)
    amateurs = {d["IdAm"] for d in data if d["IdOeu"] in oeuvres}
    return list(amateurs)


def oeuvres_likées_amateur(IdAm):
    """
    Renvoie les ID des œuvres likées par des amateurs partageant des goûts similaires.
    """
    oeuvres_likées = like_amateur(IdAm)
    amateurs_similaires = set()
    with open("amateur_oeuvre.json", "r") as f:
        data = json.load(f)
    for d in data:
        if d["IdOeu"] in oeuvres_likées and d["IdAm"] != IdAm:
            amateurs_similaires.add(d["IdAm"])
    oeuvres_recommandées = set()
    for amateur in amateurs_similaires:
        oeuvres_recommandées.update(like_amateur(amateur))
    return list(oeuvres_recommandées - set(oeuvres_likées))
