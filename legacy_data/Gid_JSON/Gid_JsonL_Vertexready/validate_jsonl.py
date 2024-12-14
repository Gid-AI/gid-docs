import json

# Chemin vers le fichier JSONL local
file_path = "C:/Users/vervi/OneDrive/Bureau/Gid_AI/Gid_JSON/Gid_JsonL_Vertexready/prompt_dataset.jsonl"

# Champs requis pour un dataset de prompts
required_fields = {"messages"}  # Les prompts doivent contenir au moins un champ "messages"

def validate_jsonl(file_path):
    errors = []
    total_lines = 0

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, start=1):
                total_lines += 1
                try:
                    # Charger chaque ligne comme un objet JSON
                    data = json.loads(line.strip())
                    
                    # Vérifier la présence des champs requis
                    missing_fields = required_fields - data.keys()
                    if missing_fields:
                        errors.append(f"Ligne {i}: Champs manquants - {missing_fields}")
                    
                    # Valider le champ "messages"
                    if "messages" in data:
                        if not isinstance(data["messages"], list) or not data["messages"]:
                            errors.append(f"Ligne {i}: 'messages' doit être une liste non vide")
                        else:
                            for j, message in enumerate(data["messages"], start=1):
                                if not isinstance(message, dict) or "author" not in message or "content" not in message:
                                    errors.append(f"Ligne {i}, Message {j}: Chaque message doit contenir 'author' et 'content'")
                                elif message["author"] not in ["user", "assistant"]:
                                    errors.append(f"Ligne {i}, Message {j}: 'author' doit être 'user' ou 'assistant'")
                                elif not isinstance(message["content"], str) or not message["content"]:
                                    errors.append(f"Ligne {i}, Message {j}: 'content' doit être une chaîne de caractères non vide")
                except json.JSONDecodeError as e:
                    errors.append(f"Ligne {i}: Erreur JSON - {str(e)}")

        # Afficher les résultats
        if errors:
            print(f"Validation terminée avec {len(errors)} erreur(s) détectée(s) sur {total_lines} lignes :")
            for error in errors:
                print(error)
        else:
            print(f"Validation réussie : {total_lines} lignes correctement formatées.")
    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} est introuvable.")
    except Exception as e:
        print(f"Une erreur inattendue s'est produite : {str(e)}")

# Lancer la validation
validate_jsonl(file_path)
