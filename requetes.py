import json

def like(IdAm, IdOeu):
    """
    Ajoute un like d'un amateur pour une œuvre.
    """
    d = {"IdAm": str(IdAm), "IdOeu": str(IdOeu)}
    try:
        with open("amateur_oeuvre.json", "r") as f:
            data = json.load(f)
        if d not in data:
            data.append(d)
            with open("amateur_oeuvre.json", "w") as f:
                json.dump(data, f, indent=4)
            print("Données mises à jour")
        else:
            print("Le like existe déjà.")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erreur lors de la lecture ou l'écriture du fichier : {e}")

def like_amateur(IdAm):
    """
    Renvoie la liste des ID d'œuvres likées par un amateur.
    """
    res = []
    try:
        with open("amateur_oeuvre.json", "r") as f:
            data = json.load(f)
        for d in data:
            if str(d.get("IdAm")) == str(IdAm):  
                res.append(str(d.get("IdOeu"))) 
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
    return res

def like_amateurs(amateurs):
    """
    Renvoie la liste des ID d'œuvres likées par plusieurs amateurs.
    """
    res = []
    try:
        with open("amateur_oeuvre.json", "r") as f:
            data = json.load(f)
        for IdAm in amateurs:
            for d in data:
                if str(d.get("IdAm")) == str(IdAm):  
                    res.append(str(d.get("IdOeu"))) 
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
    return res

def auteur(IdOeu):
    """
    Renvoie l'ID de l'artiste ayant créé l'œuvre spécifiée.
    """
    try:
        with open("oeuvres.json", "r") as f:
            data = json.load(f)
        for d in data:
            if str(d["IdOeu"]) == str(IdOeu): 
                return str(d["IdAr"])  
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
    return None

def oeuvres_auteur(IdAr):
    """
    Renvoie la liste des ID d'œuvres créées par un artiste donné.
    """
    try:
        with open("oeuvres.json", "r") as f:
            data = json.load(f)
        return [str(d["IdOeu"]) for d in data if str(d["IdAr"]) == str(IdAr)]  
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
    return []

def oeuvres_auteurs(artists):
    """
    Renvoie une liste d'œuvres créées par une liste d'artistes.
    """
    res = []
    for x in artists:
        res.extend(oeuvres_auteur(x)) 
    return res

def like_oeuvre(IdOeu):
    """
    Renvoie la liste des amateurs ayant liké une œuvre donnée.
    """
    res = []
    try:
        with open("amateur_oeuvre.json", "r") as f:
            data = json.load(f)
        res = [str(d["IdAm"]) for d in data if str(d["IdOeu"]) == str(IdOeu)]  
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
    return res

def oeuvres_likées_amateur(IdAm):
    """
    Renvoie les ID des œuvres likées par des amateurs partageant des goûts similaires.
    """
    oeuvres_likées = like_amateur(IdAm)
    amateurs_similaires = set()
    
    try:
        with open("amateur_oeuvre.json", "r") as f:
            data = json.load(f)
        for d in data:
            if str(d.get("IdOeu")) in oeuvres_likées and str(d.get("IdAm")) != str(IdAm):
                amateurs_similaires.add(d["IdAm"])
        
        oeuvres_recommandées = set()
        for amateur in amateurs_similaires:
            oeuvres_recommandées.update(like_amateur(amateur))
        
        return list(oeuvres_recommandées - set(oeuvres_likées))  
    
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return []  
