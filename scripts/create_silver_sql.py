import json
import os
from glob import glob

os.makedirs("silver", exist_ok=True)
out = "silver/legends_silver.sql"

def esc(s):
    if s is None:
        return ""
    return str(s).replace("\\", "\\\\").replace("'", "\\'").strip()

files = glob("bronze/source=fandom_only/endpoint=legends/date=*/legends_wiki.json")
latest = sorted(files)[-1]

with open(latest, encoding="utf-8") as f:
    data = json.load(f)

with open(out, "w", encoding="utf-8") as f:
    f.write("CREATE DATABASE IF NOT EXISTS brawlhalla;\n")
    f.write("USE brawlhalla;\n\n")
    f.write("DROP TABLE IF EXISTS legends_silver;\n")
    f.write("""
CREATE TABLE legends_silver (
  legend_id INT PRIMARY KEY,
  legend_name VARCHAR(150),
  bio_name VARCHAR(255),
  weapon_one VARCHAR(100),
  weapon_two VARCHAR(100),
  img_url TEXT
);
""".strip() + "\n\n")

    legend_id = 1
    for r in data:
        f.write(
            "INSERT INTO legends_silver (legend_id, legend_name, bio_name, weapon_one, weapon_two, img_url) VALUES "
            f"({legend_id}, '{esc(r.get('legend_name',''))}', '', '{esc(r.get('weapon_one',''))}', '{esc(r.get('weapon_two',''))}', '{esc(r.get('img',''))}');\n"
        )
        legend_id += 1

print(f"✅ Silver SQL généré: {out} ({len(data)} lignes)")
