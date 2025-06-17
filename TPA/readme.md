# TP A

---

## Étape 1 : Connexion initiale

1. La socket est **bloquante** au moment de `serveur.accept()` car elle **attend qu’un client se connecte** avant de continuer.

2. Si le **client ne trouve pas le serveur**, il ne peut donc pas s’y connecter, et le programme s’arrête.

3. `bind()` **associe une IP et un port** à la socket, tandis que `listen()` **permet d’écouter les connexions entrantes** sur la socket.

---

## Étape 2 : Boucle de réception

1. **Sans boucle**, le serveur ne lit **qu’un seul message**, puis s’éteint. La boucle permet qu’il **reste allumé** en attente de nouveaux messages.

2. Une **boucle infinie** permet de **continuer à attendre des messages** indéfiniment.

3. Non, le protocole **TCP ne permet pas d’envoyer plusieurs réponses à la fois** (dans un même envoi), mais on peut répondre plusieurs fois en plusieurs envois.

---

## Étape 3 : Déconnexions

1. Oui, le serveur **reste actif après la déconnexion d’un client** si on a bien mis une boucle infinie. Il attend alors une nouvelle connexion.

2. Il n’y a **rien à modifier** si la boucle `while` est déjà en place.

3. En l’état, **le serveur ne gère pas plusieurs clients** en même temps, mais **avec des threads**, cela devient possible.

---

## Étape 4 : Communication client-serveur

1. Si le serveur **attend un message** et que le client **envoie un message**, il n’y a pas de conflits.

2. On peut rendre le système **non bloquant** en utilisant des **threads** (ou des sockets non bloquantes).

3. Il est recommandé d’utiliser un **message de fin** pour **clore proprement** la communication.

---

## Étape 5 : Exécution d’instructions

1. Utiliser `eval()` pose un **gros problème de sécurité** car il permet d’exécuter **n’importe quelle commande Python**.

2. On peut utiliser un **try/except** pour **gérer les exceptions** et éviter les crashs.

---

## Étape 6 : Commandes personnalisées

1. Cela permet d’**identifier les différents messages** (commandes) et d’**adapter le comportement du serveur**.

2. On peut **parser** le message avec `message.split(" ", 1)` pour **séparer la commande** du reste du contenu.

---

## Étape 7 : Gestion de plusieurs clients

1. Sans **verrous**, plusieurs threads peuvent accéder en même temps aux mêmes données, ce qui peut causer **des conflits ou des pertes de données**.

2. Pour une **messagerie réelle**, il est souhaitable de **gérer des états partagés** (comme une liste de messages), avec des **verrous pour éviter les conflits**.

3. Une **gestion partagée des messages** est une bonne piste. Il faut aussi **supporter plusieurs clients en parallèle** et **diffuser les messages à tous les clients**.

---

## Étape 8 : Ressources partagées et sécurité

1. Les **verrous** permettent d’éviter que **plusieurs threads modifient une même ressource partagée** en même temps.

2. Sans verrous, on risque la **corruption des données**, des **pertes ou modifications** d’informations, ou encore des **comportements imprévisibles**.

---