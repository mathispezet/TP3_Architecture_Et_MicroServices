import requests

# 4.2.1
r = requests.get("https://httpbin.org/get")
print("Statut :", r.status_code)
print("En-têtes :", r.headers)
print("Contenu JSON :", r.json())

# 4.2.2
payload = {"pseudo": "roger", "canal": "coincoin"}
r = requests.get("https://httpbin.org/get", params=payload)
print(r.url)

# 4.2.3
donnees = {"pseudo": "ginette", "message": "coin coin"}
r = requests.post("https://httpbin.org/post", json=donnees)
print(r.status_code)
print(r.json()["json"])

# 4.2.4
headers = {"X-CanaDuck": "expérience-stagiaire"}
r = requests.post("https://httpbin.org/post", json={"test": 123}, headers=headers)
print(r.json()["headers"])

# 4.3
def envoyer_message(pseudo, message):
    url = "https://httpbin.org/post"
    payload = {"pseudo": pseudo, "message": message}
    try:
        reponse = requests.post(url, json=payload)
        reponse.raise_for_status()
        print("Message envoyé avec succès !")
        return reponse.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'envoi du message : {e}")
        return None

envoyer_message("maurice", "coin coin, le futur c'est maintenant !")