import json
import os
from glob import glob

os.makedirs("gold", exist_ok=True)
out = "gold/legends_gold_kpi.sql"

# prend le dernier bronze legends_wiki.json
files = glob("bronze/source=official+fandom/endpoint=legends/date=*/legends_wiki.json")
latest = sorted(files)[-1]

with open(latest, encoding="utf-8") as f:
    data = json.load(f)

total_legends = len(data)

weapons = set()
for r in data:
    w1 = (r.get("weapon_one") or "").strip()
    w2 = (r.get("weapon_two") or "").strip()
    if w1:
        weapons.add(w1)
    if w2:
        weapons.add(w2)

unique_weapons = len(weapons)

with open(out, "w", encoding="utf-8") as f:
    f.write("USE brawlhalla;\n\n")
    f.write("DROP TABLE IF EXISTS legends_gold_kpi;\n")
    f.write("""
CREATE TABLE legends_gold_kpi (
  total_legends INT,
  unique_weapons INT
);
""".strip() + "\n\n")
    f.write(
        f"INSERT INTO legends_gold_kpi (total_legends, unique_weapons) "
        f"VALUES ({total_legends}, {unique_weapons});\n"
    )

print(f"✅ Gold SQL généré: {out}")
print(f"📊 total_legends={total_legends}, unique_weapons={unique_weapons}")
