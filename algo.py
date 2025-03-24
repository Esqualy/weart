from requetes import like_amateur, auteur, oeuvres_auteur_liké #le fichier requetes a été créé par @artiste

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

def oeuvres_auteurs(idOeuvresLikees):
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

def selection_2():
    '''Propose les oeuvres des autres amateurs ayant des oeuvres likées en commun avec le main User
    '''
    act = []
    for i in idOeuvresLikeesParAmateursOeuvresLikees:
        if not i in idOeuvresLikeesParAmateursOeuvresLikees:
            act.append(i)
    return act

def anti_doublons(idOeuvresAProposer1, idOeuvresAProposer2):
    act = []
    if len(idOeuvresAProposer1) > len(idOeuvresAProposer2):
        for i in range(len(idOeuvresAProposer1)):
            if not idOeuvresAProposer1[i] in idOeuvresAProposer2:
                act.append(idOeuvresAProposer1[i])
    else :
        for i in range(len(idOeuvresAProposer2)):
            if not idOeuvresAProposer2[i] in idOeuvresAProposer1:
                act.append(idOeuvresAProposer2[i])
    return act
############## CODE

idOeuvresAProposer1 = selection_1(idOeuvresArtists, idOeuvresLikees)
### idOeuvresAProposerFinal = list(set(idOeuvresAProposer1) | set(idOeuvresAProposer2))
idOeuvresLikees = like_amateur(idAmateurMain)
idOeuvresLikees.sort()
idOeuvresArtists = oeuvres_auteurs(idOeuvresLikees)
idArtistsLikes.sort()
idOeuvresArtists = oeuvres_auteur_liké(idArtistsLikes)
idOeuvresArtists.sort()
idAmateurOeuvresLikees.sort()
idOeuvresLikeesParAmateursOeuvresLikees.sort()
idOeuvresAproposerFinal = anti_doublons(idOeuvresAProposer1, idOeuvresAProposer2)
