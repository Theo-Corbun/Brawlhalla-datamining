import requests
import json
import os
import time
from datetime import datetime

API_URL = "https://brawlhalla.fandom.com/api.php"

WEAPONS = [
    "Sword","Hammer","Blasters","Spear","Katars",
    "Rocket Lance","Axe","Bow","Gauntlets",
    "Scythe","Cannon","Orb","Greatsword",
    "Battle Boots","Chakram"
]

def get_legends():

    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": "Category:Legends",
        "cmlimit": "500",
        "format": "json"
    }

    r = requests.get(API_URL, params=params)
    data = r.json()

    legends = []

    for page in data["query"]["categorymembers"]:

        title = page["title"]

        if ":" in title:
            continue

        legends.append(title)

    return legends


def get_weapons(name):

    params = {
        "action": "query",
        "prop": "extracts",
        "titles": name,
        "explaintext": True,
        "format": "json"
    }

    r = requests.get(API_URL, params=params)
    data = r.json()

    pages = data["query"]["pages"]

    extract = ""

    for k in pages:
        extract = pages[k].get("extract","")

    found = []

    for w in WEAPONS:
        if w in extract:
            found.append(w)

    if len(found) >= 2:
        return found[0], found[1]

    return "", ""


# -------------------------

today = datetime.now().strftime("%Y-%m-%d")

path = f"bronze/source=fandom_only/endpoint=legends/date={today}"
os.makedirs(path, exist_ok=True)

legends = get_legends()

rows = []

print("Legends trouvées:", len(legends))

for name in legends:

    w1, w2 = get_weapons(name)

    if w1 == "" and w2 == "":
        w1 = "Unknown"
        w2 = "Unknown"

    rows.append({
        "legend_name": name,
        "weapon_one": w1,
        "weapon_two": w2,
        "img": ""
    })

    print(name, w1, w2)

    time.sleep(0.1)

print("Legends valides:", len(rows))

# SAUVEGARDE JSON
json_path = f"{path}/legends_wiki.json"

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(rows, f, indent=2, ensure_ascii=False)

print("JSON sauvegardé :", json_path)