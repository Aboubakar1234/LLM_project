Projet de Scraping Automatisé avec GPT-Neo
Ce projet vise à développer un agent utilisant un modèle de langage à grande échelle (LLM) pour automatiser la collecte de données à partir de sources web. L'agent extrait des informations spécifiques, génère des résumés des articles collectés, et les insère dans une base de données PostgreSQL pour une veille informationnelle sur une plateforme web.

Table des Matières
Introduction
Fonctionnalités
Architecture
Prérequis
Installation
Utilisation
Contributions
Licence
Introduction
Ce projet utilise les flux RSS de divers médias pour extraire des articles, les analyser, générer des résumés à l'aide de GPT-Neo, et stocker les résultats dans une base de données PostgreSQL. Une interface web développée avec Flask permet de consulter les articles résumés.

Fonctionnalités
Récupération des articles via les flux RSS.
Analyse et extraction du contenu des articles.
Génération de résumés avec GPT-Neo.
Insertion des articles et des résumés dans une base de données PostgreSQL.
Affichage des articles et résumés via une interface web Flask.
Architecture
Voici un diagramme du flux de données de ce projet :

Récupération des flux RSS
Analyse et extraction des articles
Génération de résumés avec GPT-Neo
Insertion des articles dans la base de données
Veille informationnelle sur une plate-forme web
Prérequis
Python 3.x
PostgreSQL
Packages Python 

Utilisation
Exécuter le script de scraping


python test.py
Lancer l'application Flask


python app.py
Accéder à l'interface web

Ouvrez votre navigateur et accédez à http://127.0.0.1:5000.
