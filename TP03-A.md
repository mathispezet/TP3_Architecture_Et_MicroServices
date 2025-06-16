TP - Client / Serveur
Étape 1 : Connexion initiale
La socket est bloquante au moment de serveur.accept() car elle attend qu’un client se connecte avant de continuer.

Si le client ne trouve pas le serveur, il ne peut donc pas s’y connecter, et le programme s’arrête.

bind() associe une IP et un port à la socket, tandis que listen() permet d’écouter les connexions entrantes sur la socket.

Étape 2 : Boucle de réception
Sans boucle, le serveur ne lit qu’un seul message, puis s’éteint. La boucle permet qu’il reste allumé en attente de nouveaux messages.

Une boucle infinie permet de continuer à attendre des messages indéfiniment.

Non, le protocole TCP ne permet pas d’envoyer plusieurs réponses à la fois (dans un même envoi), mais on peut répondre plusieurs fois en plusieurs envois.

Étape 3 : Déconnexions
Oui, le serveur reste actif après la déconnexion d’un client si on a bien mis une boucle infinie. Il attend alors une nouvelle connexion.

Il n’y a rien à modifier si la boucle while est déjà en place.

En l’état, le serveur ne gère pas plusieurs clients en même temps, mais avec des threads, cela devient possible.

Étape 4 : Communication client-serveur
Si le serveur attend un message et que le client envoie un message, il n’y a pas de conflits.

On peut rendre le système non bloquant en utilisant des threads (ou des sockets non bloquantes).

Il est recommandé d’utiliser un message de fin pour clore proprement la communication.

Étape 5 : Exécution d’instructions
Utiliser eval() pose un gros problème de sécurité car il permet d’exécuter n’importe quelle commande Python.

On peut utiliser un try/except pour gérer les exceptions et éviter les crashs.

Étape 6 : Commandes personnalisées
Cela permet d’identifier les différents messages (commandes) et d’adapter le comportement du serveur.

On peut parser le message avec message.split(" ", 1) pour séparer la commande du reste du contenu.

Étape 7 : Gestion de plusieurs clients
Sans verrous, plusieurs threads peuvent accéder en même temps aux mêmes données, ce qui peut causer des conflits ou des pertes de données.

Pour une messagerie réelle, il est souhaitable de gérer des états partagés (comme une liste de messages), avec des verrous pour éviter les conflits.

Une gestion partagée des messages est une bonne piste. Il faut aussi supporter plusieurs clients en parallèle et diffuser les messages à tous les clients.

Étape 8 : Ressources partagées et sécurité
Les verrous permettent d’éviter que plusieurs threads modifient une même ressource partagée en même temps.

Sans verrous, on risque la corruption des données, des pertes ou modifications d’informations, ou encore des comportements imprévisibles.
