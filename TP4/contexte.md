### **Réponses synthétiques - TP4 IRC en service Web**

#### **3.1 Session, état, communication**

*   **1. Gérer l'état avec HTTP :**
    On utilise un **token (jeton)**. Le client se connecte une fois, reçoit un token, et le renvoie à chaque requête pour que le serveur sache qui il est.

*   **2. Alternatives pour l'identification :**
    *   **Donner le pseudo :** Non, pas sécurisé.
    *   **Cookies / Token dans l'en-tête `Authorization` :** Oui, c'est la meilleure solution, sécurisée et standard.
    *   **Token en paramètre d'URL :** Non, expose le token et n'est pas sécurisé.

*   **3. Recevoir les messages du serveur :**
    *   **Polling :** Le client demande les messages toutes les X secondes. Simple mais inefficace.
    *   **Long-polling :** Le client fait une requête que le serveur ne termine que lorsqu'un message arrive. Bien mieux.
    *   **WebSockets :** Idéal. Ouvre une connexion permanente pour une communication en temps réel.

#### **3.2 Ressources, verbes, structure**

*   **4. Modéliser `/join #pause_cafe` :**
    On fait un `POST` sur la ressource "membres" du canal.
    *   **Route :** `POST /canaux/pause-cafe/membres`
    *   **Corps (body) :** Pas besoin, le serveur identifie l'utilisateur avec son token.

*   **5. Que renvoie `GET /msg` ?**
    La route devrait être plus précise : `GET /canaux/general/messages`. Elle renvoie les **N derniers messages** ou ceux arrivés depuis une date/ID, dans l'ordre chronologique.

*   **6. Comment structurer les URLs ?**
    *   Utiliser une hiérarchie logique : `/canaux`, `/canaux/general`, `/canaux/general/messages`.
    *   Mettre les noms de collection au **pluriel** et en **minuscules**.

#### **3.3 Robustesse, concurrence, évolutivité**

*   **7. Gérer deux `POST /msg` en même temps :**
    Utiliser un **verrou (lock)** côté serveur sur la liste des messages du canal pour s'assurer qu'ils sont ajoutés l'un après l'autre et éviter les conditions de course.

*   **8. Faut-il persister les données ?**
    Oui, absolument. On ne garde pas tout en mémoire. On doit utiliser un système de stockage durable comme une **base de données** (ou des fichiers au début) pour que les données survivent à un redémarrage.

*   **9. Quel est l'impact des connexions HTTP ?**
    Chaque requête ouvre et ferme une connexion, ce qui consomme beaucoup de ressources (CPU, réseau). Ça devient un problème avec beaucoup d'utilisateurs. Les **WebSockets** sont la solution pour passer à l'échelle.
