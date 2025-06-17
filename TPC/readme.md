#### 1.3
*   GET.
*   200 OK (succès), 301 Moved Permanently (redirection permanente), 304 Not Modified (ressource non modifiée, servie depuis le cache).
*   Il indique au serveur web quel site l'utilisateur veut consulter, car une même adresse IP peut héberger plusieurs sites.
*   Côté client : User-Agent, Accept. Côté serveur : Content-Type, Location, Set-Cookie.
*   Oui. On observe des redirections (HTTP vers HTTPS), des en-têtes de cache et des cookies sur 3ilrodez.fr.

#### 2.2
*   -I obtient seulement les en-têtes (requête HEAD). -L suit les redirections.
*   200 OK : La requête a réussi.
*   La méthode par défaut est GET. On en force une autre avec -X, par exemple -X POST.
*   Le code HTML de la page perdu.com.
*   Des en-têtes comme Content-Type, Content-Length, Server, Date.

#### 3.2
*   200 OK.
*   application/json.
*   Oui.
*   Il les analyse et les renvoie dans le corps de la réponse pour permettre de vérifier ce que le serveur a reçu.
*   L'en-tête (header) contient des métadonnées sur la requête. Le corps (body) contient la donnée utile elle-même.

#### 4.2.1
*   r.headers est un objet de type dictionnaire. r.json() retourne un dictionnaire ou une liste Python.
*   On obtient le contenu brut de la réponse sous forme d'une chaîne de caractères (string).
*   Oui, httpbin le renvoie dans le champ headers de sa réponse JSON.

#### 4.2.2
*   https://httpbin.org/get?pseudo=roger&canal=coincoin.
*   Oui, dans le champ args de la réponse JSON de httpbin.

#### 4.2.3
*   json= sérialise un dictionnaire en JSON et définit le Content-Type à application/json. data= envoie des données de formulaire.
*   Avec json=..., le Content-Type par défaut est application/json.

#### 4.2.4
*   Oui, dans le dictionnaire headers de la réponse JSON.
*   Le serveur recevrait un type de contenu annoncé (text/plain) différent du format réel du corps (JSON), ce qui pourrait causer une erreur sur une API stricte.

#### 4.3
*   On créerait une fonction qui prend les données en argument, construit la requête, l'envoie et gère la réponse (succès, erreurs).
*   Avantages : Programmable, intégration facile dans une application, gestion native du JSON et des erreurs, plus robuste et simple à utiliser.
*   Inconvénients : Ajoute une dépendance externe au projet ; son abstraction masque les détails de bas niveau du protocole HTTP.