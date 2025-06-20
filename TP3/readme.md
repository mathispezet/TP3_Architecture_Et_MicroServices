# TP 3

## 1. Réflexion liminaire

### 1.1 Cohérence concurrente et synchronisation  
- On observe des problèmes de concurrence, notamment des conditions de course sur `etat_serveur` et des conflits quand plusieurs clients modifient les canaux en même temps.  
- Si plusieurs clients sont connectés, l’état peut devenir incohérent (utilisateurs perdus, infos sur les canaux corrompues).  
- Oui, il y a des vulnérabilités possibles. Heureusement, un verrou (`threading.Lock`) est déjà en place pour limiter les dégâts.

### 1.2 Modularité et séparation des responsabilités  
- Le code mélange plusieurs responsabilités : gestion réseau (`IRCHandler`), gestion de l’état (`etat_serveur`), logs, persistance et diffusion des messages.  
- La frontière entre la logique métier et la couche réseau est floue : tout est centralisé dans `IRCHandler`.  
- La gestion d’erreur se fait aussi dans `IRCHandler`, ce qui complique les responsabilités.

### 1.3 Scalabilité et capacité à évoluer  
- Pour ajouter une nouvelle commande, il suffit de modifier `IRCHandler.handle()`.  
- En revanche, à grande échelle, ça ne tiendrait pas : il faudrait une base de données, du *load balancing* et une architecture distribuée.  
- Actuellement, tout repose en mémoire dans un seul processus, donc pas de support pour le *clustering*.

### 1.4 Portabilité de l'architecture  
- On pourrait facilement adapter le système à un protocole comme HTTP, en gardant la logique métier et en changeant juste la couche transport.  
- Certains éléments pourraient devenir des microservices (gestion des utilisateurs, canaux, logs...).  
- Il y a un certain découplage possible, notamment via des interfaces ou des APIs séparées.

### 1.5 Fiabilité, tolérance aux erreurs, robustesse  
- Les déconnexions brutales sont détectées partiellement, mais le nettoyage de l’état est incomplet.  
- Si une socket casse, ce n’est pas toujours bien détecté.  
- Il n’y a pas de garantie de livraison des messages (pas d’ACK ni de retry).

### 1.6 Protocole : structuration et évolutivité  
- Le protocole repose sur des règles implicites : une ligne = une commande, préfixe `/`, arguments séparés par des espaces.  
- C’est peu robuste, car il n’y a pas de vraie validation.  
- Il n’existe pas de spécification formelle (mais ce serait faisable).  
- Comparé à REST/HTTP, le protocole est beaucoup moins structuré : pas de codes de statut, pas de headers.

---

## 2. Analyse du code

### 2.1 Questions d’analyse  

**1. Qui traite les commandes ?**  
- Tout est géré dans `IRCHandler.handle()`, qui interprète les commandes.  
- Toutes les méthodes accèdent à `etat_serveur`.  

**2. Où sont stockées les infos ?**  
- Le canal courant d’un utilisateur est dans `etat_serveur["utilisateurs"][pseudo]["canal"]`.  
- Le `wfile` (pour écrire vers le client) est aussi stocké dans `etat_serveur`.

**3. Qu’est-ce qui peut planter ?**  
- Si un client ne fait pas `/quit`, le nettoyage est incomplet.  
- Un `write()` peut échouer, mais l’erreur est juste ignorée avec un try/except.  
- Les canaux vides ne sont pas supprimés automatiquement.

---

## 3. Limites de l'architecture

### 3.1 Couplage et responsabilités  
- Certaines fonctions (comme `envoyer_message()`) sont trop couplées : elles font état + réseau + logs en même temps.  
- Si on change le protocole, presque toutes les méthodes dans `IRCHandler` seraient à réécrire.  
- Il n’y a pas vraiment d’interface claire, le comportement est souvent implicite.  
- Aucune opération n’est vraiment atomique, donc risque d’incohérence.

### 3.2 Protocole et interopérabilité  
- Les erreurs sont très peu différenciées : un seul message d’erreur générique.  
- Il n’y a pas de grammaire normalisée du protocole.  
- Un client automatique ne peut pas facilement distinguer les types de messages.  
- Aucun support pour le versioning.  
- Globalement, c’est plus coûteux et moins standardisé que REST.

### 3.3 Testabilité et fiabilité  
- Le code est difficilement testable, car la logique métier est collée aux sockets.  
- Plusieurs cas ne sont pas testés : pannes réseau, ordre des messages...  
- Si un client est malveillant (ex. : envoie un message sans canal), l’erreur est gérée, l’état reste cohérent.  
- Les pannes partielles sont mal tolérées, aucun mécanisme de récupération.

### 3.4 Scalabilité et distribution  
- L’état actuel n’est pas réplicable car il contient des objets non sérialisables (comme `wfile`).  
- Seuls les messages peuvent être distribués facilement, pas les connexions.  
- Pour une vraie persistance, il faudrait remplacer le JSON par une base de données, et `wfile` par une *message queue*.  
- En cas de charge variable, le système risque de crasher (pas de mécanisme de limitation).  
- Une architecture scalable passerait par du microservice + *message broker* + *load balancer*.

### 3.5 Évolutivité du code et découpage en services  
- Certains services pourraient être externalisés : logs, alertes, authentification...  
- On pourrait découper la logique métier en plusieurs services : `UserService`, `ChannelService`, `MessageService`.  
- Pour être *DevOps-compatible*, il faudrait ajouter tests, monitoring, configs, conteneurs...  
- Il y a une base pour du microservice, mais il faudrait un gros refactoring : séparation nette des composants, APIs REST, et état externalisé.

---
