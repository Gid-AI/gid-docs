import jsonlines

input_file = "C:\\Users\\vervi\\OneDrive\\Bureau\\Gid8_2.0\\gid8_training_gemini_format.jsonl"
output_file = "C:\\Users\\vervi\\OneDrive\\Bureau\\Gid8_2.0\\gid8_training_gemini1.5_pro_format.jsonl" # Chemin vers le nouveau fichier JSONL converti

def convert_line(line):
    """
    Convertit une ligne du format:
    {
      "messages": [
        {"role":"system","content":"..."},
        {"role":"user","content":"..."},
        {"role":"model","content":"..."},
        ...
      ]
    }
    en format Gemini 1.5 Pro:
    {
      "systemInstruction": {
        "role":"system",
        "parts":[{"text":"..."}]
      },
      "contents":[
        {"role":"user","parts":[{"text":"..."}]},
        {"role":"model","parts":[{"text":"..."}]}
      ]
    }
    """
    messages = line.get("messages", [])
    system_instruction = None
    contents = []

    # Traiter le premier message si c'est un system
    if messages and messages[0]["role"] == "system":
        system_msg = messages[0]
        system_instruction = {
            "role": "system",
            "parts": [{"text": system_msg["content"]}]
        }
        # Retirer le message system de la liste
        rest = messages[1:]
    else:
        rest = messages

    # Pour les autres messages user/model, on les convertit
    for msg in rest:
        role = msg["role"]
        text = msg["content"]
        # role peut être user ou model
        # On le place tel quel dans contents
        contents.append({
            "role": role,
            "parts": [{"text": text}]
        })

    result = {}
    if system_instruction is not None:
        result["systemInstruction"] = system_instruction
    result["contents"] = contents

    return result

# Lecture et conversion
with jsonlines.open(input_file, "r") as reader, jsonlines.open(output_file, "w") as writer:
    for line in reader:
        new_line = convert_line(line)
        writer.write(new_line)

print(f"Conversion terminée. Fichier converti enregistré dans {output_file}")
