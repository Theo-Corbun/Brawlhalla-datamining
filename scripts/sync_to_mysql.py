import json
from glob import glob
import mysql.connector

# chercher le dernier fichier bronze
files = glob("bronze/**/legends_wiki.json", recursive=True)
latest = sorted(files)[-1]

with open(latest, encoding="utf-8") as f:
    data = json.load(f)

# connexion MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="brawlhalla"
)

cursor = conn.cursor()

# recréer legends_silver
cursor.execute("DROP TABLE IF EXISTS legends_silver")
cursor.execute("""
CREATE TABLE legends_silver (
    legend_id INT PRIMARY KEY,
    legend_name VARCHAR(150),
    bio_name VARCHAR(255),
    weapon_one VARCHAR(100),
    weapon_two VARCHAR(100),
    img_url TEXT
)
""")

legend_id = 1
weapon_set = set()

for row in data:
    legend_name = row.get("legend_name", "").strip()
    weapon_one = row.get("weapon_one", "").strip()
    weapon_two = row.get("weapon_two", "").strip()
    img_url = row.get("img", "").strip()

    if weapon_one:
        weapon_set.add(weapon_one)
    if weapon_two:
        weapon_set.add(weapon_two)

    cursor.execute("""
        INSERT INTO legends_silver
        (legend_id, legend_name, bio_name, weapon_one, weapon_two, img_url)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        legend_id,
        legend_name,
        "",
        weapon_one,
        weapon_two,
        img_url
    ))

    legend_id += 1

# recréer legends_gold_kpi
cursor.execute("DROP TABLE IF EXISTS legends_gold_kpi")
cursor.execute("""
CREATE TABLE legends_gold_kpi (
    total_legends INT,
    unique_weapons INT
)
""")

total_legends = len(data)
unique_weapons = len(weapon_set)

cursor.execute("""
    INSERT INTO legends_gold_kpi (total_legends, unique_weapons)
    VALUES (%s, %s)
""", (total_legends, unique_weapons))

conn.commit()
cursor.close()
conn.close()

print(f"✅ MySQL synchronisé : {total_legends} legends, {unique_weapons} armes uniques")