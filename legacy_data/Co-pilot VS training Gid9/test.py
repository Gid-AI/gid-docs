import json

def correct_lines(file_path, output_path):
    corrected_lines = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line_number, line in enumerate(file, start=1):
            try:
                data = json.loads(line)
                
                # Vérifier si la structure est déjà correcte avec l'un des deux ordres possibles
                if ("contents" in data and 
                    isinstance(data["contents"], list) and 
                    len(data["contents"]) == 2 and
                    all("role" in part for part in data["contents"]) and
                    all("parts" in part for part in data["contents"]) and
                    set(part["role"] for part in data["contents"]) == {"user", "model"}):
                    
                    # Ajouter le contexte par défaut si manquant
                    if "context" not in data:
                        data["context"] = "This is a training line for Gid."
                    corrected_lines.append(json.dumps(data))
                else:
                    # Reconstruire la structure correcte
                    user_text = ""
                    model_text = ""
                    
                    # Extraire le texte selon la structure trouvée
                    if "user" in data:
                        user_text = data["user"][0].get("text", "") if isinstance(data["user"], list) else ""
                    if "model" in data:
                        model_text = data["model"][0].get("text", "") if isinstance(data["model"], list) else ""
                    
                    corrected_line = {
                        "contents": [
                            {"role": "user", "parts": [{"text": user_text}]},
                            {"role": "model", "parts": [{"text": model_text}]}
                        ],
                        "context": data.get("context", "This is a training line for Gid.")
                    }
                    corrected_lines.append(json.dumps(corrected_line))
                
            except json.JSONDecodeError:
                print(f"Error parsing line {line_number}")
                continue

    # Écrire les lignes corrigées dans un nouveau fichier
    with open(output_path, 'w', encoding='utf-8') as output_file:
        for corrected_line in corrected_lines:
            output_file.write(corrected_line + '\n')

# Chemins des fichiers
file_path = 'C:/Users/vervi/OneDrive/Bureau/Gid8_2.0/gid8_complet_training_set_v3.1.jsonl'
output_path = 'C:/Users/vervi/OneDrive/Bureau/Gid8_2.0/gid8_complet_training_set_v3.1_corrected.jsonl'

correct_lines(file_path, output_path)
print(f"Correction complete. Corrected file saved to: {output_path}")