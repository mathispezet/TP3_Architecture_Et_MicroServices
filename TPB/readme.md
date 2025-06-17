### Section 1.5

1.  GET est la méthode, / est le chemin de la ressource, et HTTP/1.1 est la version du protocole.
2.  La ligne vide (créée par le deuxième "Entrée") sépare les en-têtes du corps et signale au serveur que les en-têtes sont terminés. Elle est obligatoire.
3.  Le serveur ne répond pas, car il attend la fin des en-têtes. La connexion finit par expirer (timeout).
4.  200 OK : Succès. 404 Not Found : Ressource non trouvée. 301 Moved Permanently : Redirection permanente.
5.  C'est la ligne de statut, qui contient la version du protocole, le code de statut et son message (ex: HTTP/1.1 200 OK).
6.  Ils donnent des informations sur la réponse. Content-Type indique le type de contenu (ex: text/html) et Content-Length sa taille en octets.
7.  C'est la première ligne du contenu HTML (ex: <html>). Elle est séparée des en-têtes par une ligne vide.
8.  Le serveur répond avec un code d'erreur, typiquement 404 Not Found.
9.  Oui, généralement. Le serveur envoie une page HTML conviviale expliquant que la page n'existe pas.

---

### Section 2.1.2

1.  Oui, le client reçoit bien la réponse. Le contenu affiché est "Hello World!".
2.  Elle est composée de : 1) Ligne de statut, 2) En-têtes, 3) Ligne vide, 4) Corps du message.
3.  Si la valeur est trop petite, le message est coupé. Si elle est trop grande, le client attend des données qui n'arrivent jamais.
4.  Le client ne sait pas quand la réponse se termine. Le comportement dépend du client, mais souvent il échoue ou affiche mal le contenu.
5.  Le client interprète le corps du message comme un en-tête invalide. La réponse est mal formée, et rien ne s'affiche.
6.  Les navigateurs sont tolérants pour afficher des sites web même mal codés. Les outils comme curl sont stricts et respectent le protocole à la lettre pour le débogage.

---

### Section 2.2.3

1.  Les trois éléments sont : la méthode (GET), le chemin (/motd) et la version HTTP (HTTP/1.1).
2.  On peut vérifier si la ligne contient bien trois parties après le split(). Si non, on renvoie une erreur 400 Bad Request.
3.  Elle contient le chemin de la ressource, y compris les paramètres (ex: /motd?x=42).
4.  Le code actuel ne le gère pas et générerait une erreur. Un vrai serveur renverrait un code 405 Method Not Allowed.
5.  Il renvoie la chaîne "404 Not Found" comme corps de réponse. C'est lisible mais ce n'est pas une réponse HTTP 404 complète.
6.  Non. Il manque la ligne de statut HTTP/1.1 404 Not Found pour que le client comprenne qu'il s'agit bien d'une erreur.
7.  Non, ce sont trois chaînes de caractères distinctes. Il faudrait les "normaliser" (ex: ignorer ce qui suit ? et le / final) pour les traiter comme identiques.
8.  Il faut ajouter une nouvelle condition elif chemin == "/bonjour":. La structure est extensible mais devient vite lourde.
9.  C'est une attaque de type Path Traversal. Si le code utilise ce chemin pour lire un fichier sur le disque, il pourrait exposer des fichiers système sensibles.
10. Il faut valider et nettoyer le chemin pour interdire les séquences comme .. et s'assurer qu'il ne pointe que vers des ressources autorisées.

---

### Section 2.3.2

1.  Le serveur reçoit une ligne comme GET /date HTTP/1.1. On repère le chemin en extrayant le deuxième élément de cette ligne.
2.  Le serveur sait que la requête est terminée quand il reçoit une ligne vide, qui sépare les en-têtes du corps (inexistant pour un GET).
3.  Elle contient la date et l'heure actuelles. La date change à chaque appel car elle est générée dynamiquement.
4.  L'en-tête Content-Length est indispensable. Sans lui, le client ne connaît pas la taille de la réponse et peut échouer à l'afficher.
5.  Si la valeur est trop petite, le message est tronqué. Si elle est trop grande, le client attend des données qui n'arrivent jamais (timeout).
6.  Cela dépend du client. Dans curl ou telnet, les retours à la ligne sont affichés. Dans un navigateur, ils sont traités comme de simples espaces en HTML.
7.  Le serveur exécute le else du code et renvoie la réponse par défaut ("404 Not Found"), car ces chemins ne sont pas gérés.
8.  Il répond de manière fiable mais séquentielle : un client à la fois. Il n'est pas conçu pour gérer des connexions simultanées.
9.  Oui, en ajoutant un elif pour le chemin /uptime. On pourrait y afficher le temps écoulé depuis le lancement du serveur.
10. On pourrait utiliser un dictionnaire qui associe les chemins (clés) à des fonctions (valeurs). Cela évite la longue suite de if/elif/else et rend le code plus propre.