import requests

URL = "https://www.arbeitnow.com/api/job-board-api"

# Appel à l'API
response = requests.get(URL, timeout=30)
response.raise_for_status()  # arrête le script si l'API renvoie une erreur
payload = response.json()     # transforme le JSON en dictionnaire Python

# Structure générale de la réponse
print("Clés principales :", list(payload.keys()))

offres = payload["data"]
print("Nombre d'offres sur cette page :", len(offres))

# Tous les champs de la première offre
print("\n--- Première offre ---")
for champ, valeur in offres[0].items():
    if champ == "description":
        valeur = valeur[:80] + "..."  # on raccourcit la description
    print(f"{champ}: {valeur!r}")

# Informations de pagination
print("\n--- Pagination ---")
print("links :", payload.get("links"))
print("meta :", payload.get("meta"))