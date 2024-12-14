import json

# Remplace par le chemin complet vers ton fichier JSONL
file_path = "gid8_complet_training_set_v2.0.jsonl"

# Liste pour collecter les erreurs
invalid_lines = []

# Lecture ligne par ligne pour valider chaque objet JSON
with open(file_path, "r") as file:
    for i, line in enumerate(file, start=1):
        try:
            json.loads(line.strip())  # Valide la ligne comme JSON
        except json.JSONDecodeError as e:
            invalid_lines.append((i, str(e)))

# Afficher les erreurs détectées
if invalid_lines:
    print("Lignes invalides détectées :")
    for line_number, error in invalid_lines:
        print(f"Ligne {line_number}: {error}")
else:
    print("Le fichier est valide.")
