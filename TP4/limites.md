### 2.1 Structure du code et organisation

1.  Non. Un fichier unique deviendrait trop grand, difficile à maintenir, à lire et à tester. C'est ce qu'on appelle un "monolithe".

2.  Oui. C'est une pratique recommandée pour organiser le code, en créant des modules distincts pour chaque grande fonctionnalité (ex: users.py, messages.py).

3.  
    *   Clarté : Le code est plus facile à lire et à comprendre.
    *   Maintenance : Modifier la gestion des utilisateurs n'impacte pas le fichier des messages.
    *   Travail d'équipe : Plusieurs développeurs peuvent travailler en parallèle sur des fichiers différents.

4.  En isolant la logique dans son propre module, on peut l'importer dans un script de test et appeler ses fonctions directement, sans avoir besoin de démarrer le serveur web (test unitaire).

5.  Oui. Des outils comme Swagger (OpenAPI) ou Sphinx peuvent analyser le code source à travers plusieurs fichiers pour générer une documentation web unifiée de l'API.

### 2.2 Isolation des responsabilités

1.  Dans le monolithe actuel, ce serait très difficile. Si la gestion des pseudos était un service indépendant, on pourrait le réécrire ou le remplacer sans toucher au reste de l'application.

2.  Seulement si cette API est un composant indépendant (un micro-service). On pourrait alors l'appeler depuis n'importe quelle autre application.

3.  Le service des messages a besoin de connaître l'identité des utilisateurs (pseudos). L'identifiant utilisateur est la donnée partagée la plus critique.

4.  Oui. C'est le principe du découpage en micro-services. On peut définir des frontières claires : un service "Utilisateurs", un service "Messages", un service "Canaux".

5.  En s'assurant qu'ils communiquent uniquement via des API bien définies et stables, et en évitant qu'ils partagent une base de données commune.

### 2.3 Déploiement et scalabilité

1.  Oui, si la gestion des utilisateurs est extraite dans son propre service indépendant. Il pourrait alors tourner sur un autre port, ou même une autre machine.

2.  
    *   Haute disponibilité : Si un serveur tombe en panne, l'autre prend le relai.
    *   Montée en charge (scalabilité) : On peut répartir le trafic entre les deux serveurs pour gérer plus d'utilisateurs.

3.  Oui, c'est un avantage majeur des micro-services. On peut mettre à jour et redéployer le service des messages sans interrompre le service des utilisateurs.

4.  On garderait toute la logique métier contenue dans les services (les API). On réécrirait uniquement la partie "client" (l'application mobile elle-même).

5.  
    *   Docker : Pour "empaqueter" chaque service dans un conteneur isolé.
    *   Docker Compose : Pour définir et lancer facilement l'ensemble des services en local.
    *   Kubernetes : Pour orchestrer et gérer les services en production à grande échelle.

### 2.4 Communication et cohérence

1.  Principalement via des appels réseau, en utilisant des API REST (HTTP). Ils peuvent aussi utiliser des systèmes de messagerie (comme RabbitMQ) pour une communication asynchrone.

2.  L'état n'est plus partagé. Chaque service devient la "source de vérité" pour ses propres données. Pour connaître les pseudos, un service devra interroger le service "Utilisateurs" via son API.

3.  Il est fortement déconseillé de partager une base de données. Chaque service doit avoir la sienne. Une file de messages sert à communiquer des événements, pas à stocker un état.

4.  Un service ne doit pas attendre indéfiniment. Il faut implémenter des stratégies de résilience :
    *   Réessayer (Retry) : Tenter l'appel à nouveau après un court délai.
    *   Disjoncteur (Circuit Breaker) : Arrêter de solliciter un service qui ne répond plus.
    *   Alternative (Fallback) : Fournir une réponse dégradée.

5.  On vise une cohérence à terme (eventual consistency). Les services s'échangent des événements pour se mettre à jour progressivement. La cohérence instantanée est très difficile et coûteuse à obtenir.