Prédiction de l'espèce d'Iris avec Flask et Machine Learning
Ce projet est une application Flask qui utilise des modèles de Machine Learning pour prédire l'espèce d'une fleur d'Iris basée sur ses caractéristiques. L'application est conçue pour fonctionner avec plusieurs nœuds, en envoyant des requêtes à chaque nœud et en déterminant l'espèce la plus probable à partir des réponses reçues.

Fonctionnalités
Serveur Flask pour recevoir les données de caractéristiques d'Iris et renvoyer une prédiction de l'espèce.
Utilisation de RandomForestClassifier, SVC, et LinearRegression pour la prédiction.
Communication avec d'autres nœuds définis dans participants.json pour collecter des prédictions.
Mise à jour des poids et des dépôts des nœuds en fonction de la précision de leurs prédictions.

Installation
Clonez ce dépôt sur votre machine locale.
Assurez-vous que Python 3 est installé sur votre système.
Installez les dépendances nécessaires
puis lancez serveur.py

Une fois l'application lancée, elle démarre un serveur Flask et commence à écouter sur le port 5000. Vous pouvez envoyer des requêtes POST à http://localhost:5000/predict avec des données JSON contenant les caractéristiques d'une fleur d'Iris pour recevoir une prédiction de l'espèce.

Exemple de requête
{
  "input": [5.1, 3.5, 1.4, 0.2]
}

Structure du fichier participants.json
Ce fichier doit contenir une liste des nœuds participants avec leur IP et d'autres informations. Voici un exemple:
{
  "192.168.1.1": {"weight": 0.5, "deposit": 1000},
  "192.168.1.2": {"weight": 0.7, "deposit": 1500}
}

Développement
Ce projet est conçu pour être facilement extensible. Vous pouvez ajouter d'autres modèles de Machine Learning dans le dictionnaire models et ajuster la logique de traitement des réponses selon vos besoins.