# WeArt
We Art - We are

### Information 
Une version avec IA aurai du voir le jour, mais malgré plusieurs problèmes techniques et du côut que peut représenter sur les hebergements, nous avons été contraint de pas l'implémenter pour la version trophée NSI. Cependant, elle reste toujours disponible dans le depot, pour pouvoir tester notre technique pour crée des similarités entre plusieurs images. 

Vous retrouverez aussi dans ```utils/``` des morceaux de codes qui ont servi ou été abandonné sur l'avancée comme ```upload.py``` qui a servi à la page d'upload du site internet.

## Presentation du projet
WeArt est une plateforme dédiée aux artistes et amateurs d’art. Son objectif est d’exposer, échanger et favoriser la reconnaissance des artistes à l'échelle mondiale. Accessible via un site web, elle couvre toutes les formes d’art et propose un réseau social artistique. Grâce à un algorithme intelligent, chaque utilisateur découvre des œuvres adaptées à ses goûts. WeArt met en avant l’art visuel, en particulier numérique, tout en valorisant l’inspiration et la collaboration.

## Membres de l’équipe
Thibault - Esqualy : Administrateur système, réseau et développeur de l’algorithme avec Intelligence Artificielle.
Clémence - sh4nxel : Développeuse des systèmes de scroll, like et premières suggestions du site
Benjamin - h4r1cX : Développeur de l’algorithme de suggestion.
Noé - ThsArtiste : Créateur de la base de données et développeur des liaisons entre la base de données, l’algorithme et le serveur.

## Prérequis
Python est nécessaire pour installer et executer le projet
[Git](https://git-scm.com/book/fr/v2/D%C3%A9marrage-rapide-Installation-de-Git) afin de pouvoir installer CLIP de OpenAI pour l'algorythme IA.

## Installation 
```
git clone https://github.com/Esqualy/weart.git
cd weart
pip install -r requirements.txt
```

## Utilisation
En fonction du contenue du dossier website : 
=> weart :
```
python -m weart.app
# depuis le dossier website
```
=> cdn :
```
python -i app.py
# depuis le dossier cdn
```

## Technologies Utilisées
* Flask (librairie python) pour le serveur.
* HTML/CSS, JavaScript pour le front-end.
* Python pour l'algorithme de suggestion et l'intégration avec la base de données.
* JSON pour la gestion des données.

### Remerciment
Merci à M. S. Meden, notre prof de NSI de nous avoir guidé tout au long de notre aventure sur WeArt.
