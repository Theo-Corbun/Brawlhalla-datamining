import mysql.connector
import matplotlib.pyplot as plt

# ==========================
# Connexion MySQL
# ==========================
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="brawlhalla"
)

cursor = conn.cursor()

# ==========================
# Récupération des armes
# ==========================
cursor.execute("""
    SELECT weapon_one
    FROM legends_silver
    WHERE weapon_one IS NOT NULL AND weapon_one <> ''
""")
weapon_one_rows = cursor.fetchall()

cursor.execute("""
    SELECT weapon_two
    FROM legends_silver
    WHERE weapon_two IS NOT NULL AND weapon_two <> ''
""")
weapon_two_rows = cursor.fetchall()

weapons = [row[0] for row in weapon_one_rows] + [row[0] for row in weapon_two_rows]

# ==========================
# Comptage des occurrences des armes
# ==========================
weapon_counts = {}
for weapon in weapons:
    weapon_counts[weapon] = weapon_counts.get(weapon, 0) + 1

sorted_weapon_counts = sorted(weapon_counts.items(), key=lambda x: x[1], reverse=True)

weapon_labels = [item[0] for item in sorted_weapon_counts]
weapon_values = [item[1] for item in sorted_weapon_counts]

# ==========================
# Nombre de légendes uniques
# ==========================
cursor.execute("""
    SELECT COUNT(DISTINCT legend_name)
    FROM legends_silver
    WHERE legend_name IS NOT NULL AND legend_name <> ''
""")
unique_legends = cursor.fetchone()[0]

# ==========================
# Nombre d’armes uniques
# ==========================
unique_weapons = set(weapons)
unique_weapons_count = len(unique_weapons)

# ==========================
# Catégories d’armes
# ==========================
weapon_categories = {
    "courte distance": [
        "Sword",
        "Hammer",
        "Katars",
        "Gauntlets",
        "Scythe",
        "Axe",
        "Greatsword",
        "Battle Boots",
        "Chakram"
    ],
    "mi distance": [
        "Spear",
        "Rocket Lance",
        "Orb",
        "Cannon"
    ],
    "longue distance": [
        "Blasters",
        "Bow"
    ]
}

short_count = len([
    w for w in unique_weapons
    if w in weapon_categories["courte distance"]
])

mid_count = len([
    w for w in unique_weapons
    if w in weapon_categories["mi distance"]
])

long_count = len([
    w for w in unique_weapons
    if w in weapon_categories["longue distance"]
])

type_labels = ["courte distance", "mi distance", "longue distance"]
type_values = [short_count, mid_count, long_count]

# ==========================
# Graphique 1 : Armes triées par occurrence
# ==========================
plt.figure(figsize=(12, 6))
bars = plt.bar(weapon_labels, weapon_values)

plt.title("Armes les plus présentes dans Brawlhalla")
plt.xlabel("Armes")
plt.ylabel("Occurrences")
plt.xticks(rotation=45)
plt.tight_layout()

for bar, value in zip(bars, weapon_values):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.1,
        str(value),
        ha="center"
    )

plt.savefig("weapons_chart.png")
plt.show()

# ==========================
# Graphique 2 : Nombre de légendes uniques
# ==========================
plt.figure(figsize=(6, 5))
bars = plt.bar(["Légendes uniques"], [unique_legends])

plt.title("Nombre total de légendes uniques")
plt.ylabel("Total")
plt.tight_layout()

for bar in bars:
    value = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + 0.1,
        str(int(value)),
        ha="center"
    )

plt.savefig("unique_legends_chart.png")
plt.show()

# ==========================
# Graphique 3 : Nombre d’armes uniques
# ==========================
plt.figure(figsize=(6, 5))
bars = plt.bar(["Armes uniques"], [unique_weapons_count])

plt.title("Nombre total d’armes uniques")
plt.ylabel("Total")
plt.tight_layout()

for bar in bars:
    value = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + 0.1,
        str(int(value)),
        ha="center"
    )

plt.savefig("unique_weapons_chart.png")
plt.show()

# ==========================
# Graphique 4 : Type d’armes uniques
# ==========================
plt.figure(figsize=(10, 5))
bars = plt.bar(type_labels, type_values)

plt.title(f"armes uniques = {unique_weapons_count}")
plt.ylabel("nombre d'armes")

for bar, value in zip(bars, type_values):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.1,
        str(value),
        ha="center"
    )

plt.savefig("weapon_types_chart.png")
plt.show()

# ==========================
# Fermeture connexion
# ==========================
cursor.close()
conn.close()

print("Graphiques générés :")
print("- weapons_chart.png")
print("- unique_legends_chart.png")
print("- unique_weapons_chart.png")
print("- weapon_types_chart.png")