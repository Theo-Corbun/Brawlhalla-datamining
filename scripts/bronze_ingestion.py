import urllib.request
import urllib.parse
import json
import os
import re
import time
from datetime import datetime

FANDOM_API = "https://brawlhalla.fandom.com/api.php"
CATEGORY = "Category:Legends"

WEAPONS = [
    "Battle Boots", "Rocket Lance", "Greatsword",
    "Chakram", "Blasters", "Gauntlets", "Katars", "Scythe",
    "Cannon", "Hammer", "Spear", "Sword", "Axe", "Bow", "Orb"
]
WEAPON_SET = set(WEAPONS)

# -------------------------
# helpers
# -------------------------
def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="ignore")

def fandom_get_json(params: dict):
    url = FANDOM_API + "?" + urllib.parse.urlencode(params)
    return json.loads(fetch_text(url))

def clean(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip()

# -------------------------
# fandom category members
# -------------------------
def get_category_titles() -> list[str]:
    titles = []
    cmcontinue = None
    while True:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": CATEGORY,
            "cmlimit": "500",
            "format": "json"
        }
        if cmcontinue:
            params["cmcontinue"] = cmcontinue

        data = fandom_get_json(params)
        members = data.get("query", {}).get("categorymembers", [])
        for m in members:
            t = clean(m.get("title", ""))
            if t:
                titles.append(t)

        cont = data.get("continue", {})
        cmcontinue = cont.get("cmcontinue")
        if not cmcontinue:
            break

    # dédup
    seen = set()
    out = []
    for t in titles:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out

# -------------------------
# weapons extraction robust
# -------------------------
def weapons_from_text(text: str):
    t = clean(text)
    if not t:
        return "", ""
    positions = []
    for w in WEAPONS:
        idx = t.find(w)
        if idx != -1:
            positions.append((idx, w))
    positions.sort(key=lambda x: x[0])
    found = []
    for _, w in positions:
        if w not in found:
            found.append(w)
        if len(found) == 2:
            break
    return (found[0] if len(found) >= 1 else "", found[1] if len(found) >= 2 else "")

def get_wikitext(title: str) -> str:
    data = fandom_get_json({
        "action": "parse",
        "page": title,
        "prop": "wikitext",
        "format": "json"
    })
    return data.get("parse", {}).get("wikitext", {}).get("*", "") or ""

def get_plain_extract(title: str) -> str:
    data = fandom_get_json({
        "action": "query",
        "prop": "extracts",
        "exintro": "1",
        "explaintext": "1",
        "titles": title,
        "format": "json"
    })
    pages = data.get("query", {}).get("pages", {})
    if not pages:
        return ""
    page_obj = next(iter(pages.values()))
    return page_obj.get("extract", "") or ""

def get_weapons(title: str):
    # wikitext d'abord
    try:
        wt = get_wikitext(title)
        w1, w2 = weapons_from_text(wt)
        if w1 and w2:
            return w1, w2
    except:
        pass

    # extract intro ensuite
    try:
        ex = get_plain_extract(title)
        w1, w2 = weapons_from_text(ex)
        if w1 and w2:
            return w1, w2
    except:
        pass

    return "", ""

# -------------------------
# image (pageimages)
# -------------------------
def get_image(title: str) -> str:
    try:
        data = fandom_get_json({
            "action": "query",
            "titles": title,
            "prop": "pageimages",
            "pithumbsize": "500",
            "format": "json"
        })
        pages = data.get("query", {}).get("pages", {})
        if not pages:
            return ""
        page_obj = next(iter(pages.values()))
        thumb = page_obj.get("thumbnail", {})
        return thumb.get("source", "") or ""
    except:
        return ""

# -------------------------
# Filters anti parasites
# -------------------------
def looks_like_bad_title(title: str) -> bool:
    bad_prefix = ("Category:", "File:", "Help:", "Template:", "User:", "Forum:")
    if title.startswith(bad_prefix):
        return True

    # pages trolls courantes
    bad_words = ["delete this", "yo mods", "test", "sandbox"]
    low = title.lower()
    if any(w in low for w in bad_words):
        return True

    return False

# =============================
# BRONZE PIPELINE
# =============================
today = datetime.now().strftime("%Y-%m-%d")
base_dir = f"bronze/source=fandom_only/endpoint=legends/date={today}"
os.makedirs(base_dir, exist_ok=True)

titles = [t for t in get_category_titles() if not looks_like_bad_title(t)]
print(f"✅ Candidats catégorie: {len(titles)}")

rows = []
skipped = 0

for i, title in enumerate(titles, start=1):
    w1, w2 = get_weapons(title)

    # Si pas 2 armes -> on ignore (ça élimine plein de parasites)
    if not w1 or not w2:
        skipped += 1
        continue

    img = get_image(title)

    rows.append({
        "legend_name": title,
        "weapon_one": w1,
        "weapon_two": w2,
        "img": img
    })

    print(f"[{len(rows)}] {title} -> {w1}/{w2}")
    time.sleep(0.15)

with open(f"{base_dir}/legends_wiki.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, indent=2, ensure_ascii=False)

meta = {
    "source": "fandom_only (filtered by weapons)",
    "date": today,
    "records": len(rows),
    "skipped": skipped
}
with open(f"{base_dir}/metadata_response.json", "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2, ensure_ascii=False)

print(f"✅ Bronze OK: {len(rows)} legends gardées")
print(f"⏭️ Skipped (pas d'armes): {skipped}")
print("📁", base_dir)
