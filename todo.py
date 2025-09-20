import pandas as pd

# Definierte Tabelle mit Korrekturen
data = [
    {"Ort": "S. 5, Z. 9", "Problemart": "Rechtschreibung", "Korrektur / Vorschlag": "„Fensers“ → Fensters"},
    {"Ort": "S. 6, Z. 2", "Problemart": "Rechtschreibung", "Korrektur / Vorschlag": "„Horchtposten“ → Horchposten"},
    {"Ort": "S. 5, Z. 9 / S. 6 (mehrfach)", "Problemart": "Layout/Trennung", "Korrektur / Vorschlag": "„get_sur- face()“ → Silbentrennung vermeiden"},
    {"Ort": "S. 6", "Problemart": "Stil", "Korrektur / Vorschlag": "„IchMacheJaEigentlichGarNichts-Spiel“ → „ein inaktives Spiel“"},
    {"Ort": "S. 4, Einleitung", "Problemart": "Zeichensetzung", "Korrektur / Vorschlag": "„Probleme bzw. Techniken“ → besser: „Probleme und Techniken“"},
    {"Ort": "S. 5", "Problemart": "Zeichensetzung", "Korrektur / Vorschlag": "Komma fehlt: „wie beispielsweise die Soundunterstützung“ → Komma vor „wie“"},
    {"Ort": "S. 7, Z. 20", "Problemart": "Stil", "Korrektur / Vorschlag": "„per Übergabeparameter“ → „durch Parameterübergabe“"},
    {"Ort": "S. 6–7", "Problemart": "Stil", "Korrektur / Vorschlag": "Initialisierungsbeschreibung stilistisch glätten"},
    {"Ort": "S. 9 (Aufzählung)", "Problemart": "Zeichensetzung", "Korrektur / Vorschlag": "Punkte in Aufzählung einheitlich oder weglassen"},
    {"Ort": "S. 11, Z. 14", "Problemart": "Stil", "Korrektur / Vorschlag": "„Eigene Farben“ → „Benutzerdefinierte Farben“"},
    {"Ort": "S. 11, Z. 26–34", "Problemart": "Fachsprache", "Korrektur / Vorschlag": "Optional: Link zu Doku bei geometrischen Begriffen"},
    {"Ort": "S. 13, Z. 34", "Problemart": "Sprache", "Korrektur / Vorschlag": "„erzeugt“ → „gezeichnet“"},
    {"Ort": "S. 14, Abb. 2.6", "Problemart": "Grammatik", "Korrektur / Vorschlag": "„mit gefällt...“ → „mir gefällt...“"},
    {"Ort": "S. 17, Z. 22", "Problemart": "Grammatik", "Korrektur / Vorschlag": "„außerhalb des Bildschirm“ → „außerhalb des Bildschirms“"},
    {"Ort": "S. 23, Z. 22", "Problemart": "Stil", "Korrektur / Vorschlag": "„linke Koordinate“ → „x-Position“"},
    {"Ort": "S. 25", "Problemart": "Redundanz", "Korrektur / Vorschlag": "Wiederholung von Breitenformeln kürzen"},
    {"Ort": "S. 26–27", "Problemart": "Fachlich", "Korrektur / Vorschlag": "„äquidistant“ ggf. erklären"},
    {"Ort": "S. 27, Was war neu?", "Problemart": "Stil", "Korrektur / Vorschlag": "„Linksoben“ → „links oben“"}
]

# In DataFrame umwandeln
df = pd.DataFrame(data)

# Speichern als CSV
csv_path = "./pygame_korrekturen.csv"
df.to_csv(csv_path, index=False)

# Speichern als Markdown
md_path = "./pygame_korrekturen.md"
with open(md_path, "w", encoding="utf-8") as f:
    f.write("| Ort | Problemart | Korrektur / Vorschlag |\n")
    f.write("|-----|-------------|------------------------|\n")
    for row in data:
        f.write(f"| {row['Ort']} | {row['Problemart']} | {row['Korrektur / Vorschlag']} |\n")

csv_path, md_path
