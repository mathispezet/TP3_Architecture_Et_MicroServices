# Fiche de protocole — IRC CanaDuck

Complétez cette fiche pour décrire comment les clients interagissent avec le serveur IRC actuel.

## Format général

- Chaque commande est envoyée par le client sous forme d'une **ligne texte** terminée par `\n`.

## Commandes supportées

| **Commande** | **Syntaxe exacte**       | **Effet attendu**               | **Réponse du serveur**                              | **Responsable côté serveur**    |
|--------------|-------------------------|--------------------------------|----------------------------------------------------|--------------------------------|
| `/nick`      | `/nick <pseudo>`        | Attribue un pseudo unique       | `Bienvenue, <pseudo> !` ou `Pseudo déjà pris.`     | `set_pseudo()`                 |
| `/join`      | `/join <canal>`         | Rejoint ou crée un canal        | `Canal <canal> rejoint.`                           | `rejoindre_canal()`            |
| `/msg`       | `/msg <texte>`          | Envoie message dans canal courant | Diffusion `[<canal>] <pseudo>: <texte>`            | `envoyer_message()`            |
| `/read`      | `/read`                 | Info sur lecture différée       | `(Toutes les discussions sont en direct, pas de lecture différée)` | `lire_messages()`              |
| `/log`       | `/log`                  | Affiche 10 dernières lignes du journal | Contenu des dernières lignes du fichier log      | `lire_logs()`                  |
| `/alert`     | `/alert <texte>`        | Envoi alerte globale (admin/moderator) | `Alerte envoyée.` ou `Vous n'avez pas les droits pour envoyer une alerte.` | `envoyer_alerte()`             |
| `/quit`      | `/quit`                 | Déconnexion propre              | `Au revoir !`                                      | Nettoyage dans `handle()`      |

## Exemples d'interactions

### Exemple 1 : choix du pseudo

Client > /nick ginette
Serveur > Bienvenue, ginette !

### Exemple 2 : rejoindre un canal

Client > /join general
Serveur > Canal general rejoint.

### Exemple 3 : envoyer un message

Client > /msg Salut tout le monde !
Serveur > [general] ginette: Salut tout le monde !

### Exemple 4 : message sans canal

Client > /msg Hello
Serveur > Vous n'avez pas rejoint de canal.

### Exemple 5 : consultation des logs

Client > /log
Serveur > [2025-06-16 14:30:15] ginette s'est connecté.
[2025-06-16 14:31:22] bob a rejoint le canal general.

### Exemple 6 : alerte non autorisée

Client > /alert Maintenance prévue
Serveur > Vous n'avez pas les droits pour envoyer une alerte.

### Exemple 7 : pseudo déjà pris

Client > /nick alice
Serveur > Pseudo déjà pris.

### Exemple 8 : commande inconnue

Client > /help
Serveur > Commande inconnue.

# Structure interne – Qui fait quoi ?

| Élément                       | Rôle dans l'architecture                                   |
|------------------------------|------------------------------------------------------------|
| `IRCHandler.handle()`         | Lit et traite les lignes de commande reçues via TCP       |
| `etat_serveur`                | Dictionnaire partagé contenant utilisateurs connectés, canaux actifs, et verrou de synchronisation |
| `log()`                      | Journalisation dans fichier + diffusion d'alerte système   |
| `broadcast_system_message()`  | Envoi de messages à tous les utilisateurs connectés        |
| `etat_serveur["utilisateurs"]`| Mapping pseudo → { "canal": str, "wfile": file, "role": str } |
| `etat_serveur["canaux"]`      | Mapping nom_canal → [liste_pseudos] pour la diffusion      |
| `etat_serveur["lock"]`        | Verrou `threading.Lock` pour protéger les accès concurrents|
| `charger_etat()` / `sauvegarder_etat()` | Persistance JSON de l'état serveur                   |
| `ThreadingTCPServer`          | Serveur TCP multi-threadé, un thread par client             |
| `ROLES_AUTORISES_ALERT`       | Constante définissant les rôles autorisés pour `/alert`    |

# Points de défaillance potentiels

| **Zone fragile**              | **Cause possible**             | **Conséquence attendue**          | **Présence de gestion d'erreur ?**  |
|------------------------------|-------------------------------|----------------------------------|------------------------------------|
| `wfile.write(...)`            | Socket cliente fermée/cassée  | Exception, arrêt du thread client | Oui (try/except dans broadcast)    |
| Modification d'`etat_serveur` | Accès concurrent sans verrou  | État corrompu, utilisateurs perdus | Oui (threading.Lock utilisé)       |
| Lecture du fichier log        | Fichier inexistant ou corrompu| Exception lors de `/log`           | Oui (try/except dans lire_logs)    |
| Pseudo déjà pris (`/nick`)   | Collision de noms utilisateur  | Refus de connexion                | Oui (vérification + message d'erreur) |
| Utilisateur sans canal courant| `/msg` envoyé sans `/join`    | Message d'erreur explicite        | Oui (vérification + message d'erreur) |
| Déconnexion brutale client    | Fermeture socket sans `/quit` | Utilisateur fantôme dans l'état   | Partielle (nettoyage dans finally) |
| Canal vide après départ       | Dernier utilisateur quitte    | Canal reste dans `etat_serveur`  | Non (pas de nettoyage automatique)|
| Saturation mémoire            | Trop d'utilisateurs/canaux    | Performance dégradée/crash        | Non (pas de limitation)            |
| Fichier `etat_serveur.json` corrompu | JSON malformé au démarrage | Perte de l'état des canaux        | Oui (try/except dans `charger_etat`) |
| Droits insuffisants (`/alert`)| Utilisateur role="user"       | Message de refus                 | Oui (vérification des rôles)       |

# Remarques ou cas particuliers

- Les commandes sont traitées **en texte brut**, sans structure formelle.
- Une mauvaise commande renvoie un message générique (`Commande inconnue.`).
- Les **wfile** ne sont pas persistés (reconnexion nécessaire après redémarrage serveur).
- Le système de **rôles** existe (`user`, `admin`, `moderator`) mais seul `/alert` l'utilise.
- **Pas de validation** des noms de canaux ou pseudos (caractères spéciaux autorisés).
- **Threading** : chaque client = un thread, pas de limitation du nombre de connexions.
- **Persistance partielle** : seuls les canaux sont sauvegardés, pas les utilisateurs connectés.
- **Broadcast des alertes** : `/alert` + `log()` envoient le message à TOUS les utilisateurs.
- **Gestion des erreurs** : messages d'erreur envoyés au client, mais pas de codes d'erreur structurés.
- **Sécurité** : aucune authentification, aucun chiffrement, rôles attribués par défaut.