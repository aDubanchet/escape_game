# Escape Game : 

## Etapes d’installation du serveur : 

Création du serveur via AWS 
* Connexion à l’instance : Choisir Ubuntu 
* Mise à jour de l’OS : 
		sudo apt update
* Installation des packages nécessaires :
		snap install docker 
		sudo apt install git

* Installation de l’image Docker : 

	Téléchargement de l’escape Game : 
	cd 
	git clone https://github.com/aDubanchet/escape_game
	cd escape_game 

	
* Changer l’ip du serveur : 
	Remplacer * de la variable ALLOWED_HOST du fichier /app/escape_game/settings.py par l’ip du serveur. 
* Mise en place du serveur :
	Construire et lancer l’image :
	
	docker-compose build 
	docker-compose up 
	
	Créer un admin : 
	docker-compose exec app python manage.py createsuperuser 



## Commandes utiles : 
Construire et lancer l’image :
docker-compose up —build -d


Arrêter le serveur : 
docker-compose down 

Démarrer le serveur : 
docker-compose up -d 

Ajouter un Administrateur :
Docker-compose exec app python manage.py createsuperuser



## Mettre à jour le jeu WebGL :
Déposer la version compilée du jeu dans le dossier : 
escape_game/app/static/webgl/ 

Puis faire les commandes : 
docker-compose build 
docker-compose up 
docker-compose exec app python manage.py collectstatic —noinput

## Vérifier la progression  :
Ouvrir la console web du navigateur : 
post_progression(80);


