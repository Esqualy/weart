from requetes import like_amateur, like_amateurs, auteur, oeuvres_auteurs #le fichier requetes a été créé par @Noé Callejon, elle a pour but de créer des fonctions qui permettent d'interagir avec les json.

##############VARS
idAmateurMain = input("ID MAIN") # ??????????????????
idOeuvresLikees = []
idArtistsLikes = [] #Attention, par le biais des oeuvres ci-dessus
idOeuvresArtists = [] #Attention, toutes les oeuvres des ArtistsLikes, y compris les OeuvresLikees
idAmateurOeuvresLikees = []
idOeuvresLikeesParAmateursOeuvresLikees = []

idOeuvresAProposer1 = []
idOeuvresAProposer2 = []
idOeuvresAproposerFinal = []

##############DEFS

def user_oeuvres_artists(idOeuvresLikees):
    '''Renvoie une liste d'ID des artists des likes de l'user
    '''
    act = []
    for i in idOeuvresLikees:
        act.append(auteur(i))
    return act

def selection_1(idOeuvresArtists, idOeuvresLikees)-> list[int]:
    '''Retranche les idOeuvresLikees aux idOeuvresArtists (dans le but de les mettre dans idOeuvresAProposer1)
    '''
    act = []
    for i in range(len(idOeuvresArtists)):
        if not idOeuvresArtists[i] in idOeuvresLikees:
            act.append(idOeuvresArtists[i])
    return act

def selection_2(idOeuvresLikeesParAmateursOeuvresLikees, idOeuvresLikees):
    '''Propose les oeuvres des autres amateurs ayant des oeuvres likées en commun avec le main User
    '''
    act = []
    for i in idOeuvresLikeesParAmateursOeuvresLikees:
        if not i in idOeuvresLikees:
            act.append(i)
    return act

############## CODE

idOeuvresAProposer1 = selection_1(idOeuvresArtists, idOeuvresLikees)
idOeuvresLikees = like_amateur(idAmateurMain)
idOeuvresLikees.sort()
idArtistsLikes = user_oeuvres_artists(idOeuvresLikees)
idOeuvresLikees.sort()
idOeuvresArtists = oeuvres_auteurs(idOeuvresLikees)
idOeuvresArtists.sort()
idAmateurOeuvresLikees.sort()
idOeuvresLikeesParAmateursOeuvresLikees = like_amateurs(idAmateurOeuvresLikees)
idOeuvresLikeesParAmateursOeuvresLikees.sort()

idOeuvresAProposer1 = selection_1(idOeuvresArtists, idOeuvresLikees)
idOeuvresAProposer2 = selection_2(idOeuvresLikeesParAmateursOeuvresLikees, idOeuvresLikees)

idOeuvresAProposerFinal = list(set(idOeuvresAProposer1) | set(idOeuvresAProposer2))
print(idOeuvresAProposer1)
print(idOeuvresAProposer2)
