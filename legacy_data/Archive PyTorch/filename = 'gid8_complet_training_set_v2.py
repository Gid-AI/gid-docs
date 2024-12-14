import json

def validate_line_structure(line_data, line_number):
    errors = []
    
    # Vérifier les clés principales
    if not all(key in line_data for key in ['contents', 'context']):
        errors.append(f"Ligne {line_number}: Manque 'contents' ou 'context'")
        return errors

    # Vérifier contents
    contents = line_data['contents']
    if not isinstance(contents, list) or len(contents) != 2:
        errors.append(f"Ligne {line_number}: 'contents' doit contenir exactement 2 éléments")
        return errors

    # Vérifier les rôles
    roles = [item.get('role') for item in contents]
    if not all(role in ['user', 'model'] for role in roles):
        errors.append(f"Ligne {line_number}: Roles invalides - doivent être 'user' et 'model'")
        
    if roles[0] not in ['user', 'model'] or roles[1] not in ['user', 'model']:
        errors.append(f"Ligne {line_number}: Il doit y avoir un 'user' et un 'model'")
    
    # Vérifier structure parts et text
    for item in contents:
        if 'parts' not in item:
            errors.append(f"Ligne {line_number}: Manque 'parts' dans un élément")
        elif not isinstance(item['parts'], list):
            errors.append(f"Ligne {line_number}: 'parts' n'est pas une liste")
        elif not all('text' in part for part in item['parts']):
            errors.append(f"Ligne {line_number}: Manque 'text' dans 'parts'")

    return errors

def process_files():
    input_file = 'C:/Users/vervi/OneDrive/Bureau/Gid8_2.0/gid8_complet_training_set_v3.0.jsonl'
    problematic_file = 'C:/Users/vervi/OneDrive/Bureau/Gid8_2.0/lignes_problematiques.jsonl'
    clean_file = 'C:/Users/vervi/OneDrive/Bureau/Gid8_2.0/gid8_complet_training_set_v3.0_clean.jsonl'

    problematic_lines = []
    valid_lines = []

    with open(input_file, 'r', encoding='utf-8') as file:
        for line_number, line in enumerate(file, 1):
            try:
                line_data = json.loads(line.strip())
                errors = validate_line_structure(line_data, line_number)
                
                if errors:
                    problematic_lines.append(line)
                else:
                    valid_lines.append(line)
            except json.JSONDecodeError:
                problematic_lines.append(line)

    with open(problematic_file, 'w', encoding='utf-8') as file:
        file.writelines(problematic_lines)

    with open(clean_file, 'w', encoding='utf-8') as file:
        file.writelines(valid_lines)

    print(f"Lignes problématiques trouvées: {len(problematic_lines)}")
    print(f"Lignes valides: {len(valid_lines)}")
    print("Fichiers créés: lignes_problematiques.jsonl et gid8_complet_training_set_v3.0_clean.jsonl")

process_files()