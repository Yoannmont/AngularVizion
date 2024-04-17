# AngularVision

AngularVision est une application web de reconnaissance d'images développée avec Angular, PyTorch et Flask.
L'objectif de ce projet simple est de s'entraîner à l'utilisation simultanée de plusieurs outils tech populaires. 
L'application permet aux utilisateurs de charger des images et utilise le modèle [DETR-RESNET-50 de Facebook](https://huggingface.co/facebook/detr-resnet-50) pour reconnaître les objets présents dans ces images.

## Fonctionnalités

- Interface utilisateur développée avec Angular.
- Prétraitement des images utilisant PyTorch pour la préparation des données d'entrée.
- Reconnaissance d'objets parmi un ensemble de 91 classes sur les images chargées.
- Affichage des résultats de la reconnaissance d'objets sur l'interface utilisateur.

## Technologies Utilisées

- Angular : Framework front-end pour le développement de l'interface utilisateur.
- PyTorch : Bibliothèque d'apprentissage automatique (Machine Learning) utilisé pour le traitement des images. 
- Flask : Backend en Python pour l'API de prétraitement des images et l'inference du modèle.
- Docker : Plateforme de conteneurisation de l'application 

## Installation Normale

1. Cloner le dépôt Git :
`git clone https://github.com/Yoannmont/AngularVizion.git`
2. Installation des dépendances :
`cd AngularVision/client` `npm install`

3. Démarrer client :
`cd client`
`ng serve -o`
4. Démarrer serveur :
`cd server`
`flask run`

## Utilisation avec Docker

