import json
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForCausalLM, AdamW

# Définir un dataset personnalisé
class JSONLDataset(Dataset):
    def __init__(self, file_path):
        self.data = []
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    entry = json.loads(line.strip())
                    user_input = " ".join([p["text"] for p in entry["contents"] if p["role"] == "user"])
                    model_output = " ".join([p["text"] for p in entry["contents"] if p["role"] == "model"])
                    context = entry.get("context", "")
                    prompt = f"CONTEXT: {context} USER: {user_input}" if context else f"USER: {user_input}"
                    self.data.append({"prompt": prompt, "response": model_output})
        except Exception as e:
            print(f"Erreur lors du chargement des données depuis {file_path}: {e}")
            exit(1)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

# Charger les données et entraîner le modèle
def train_model(file_path):
    try:
        # Charger le tokenizer et le modèle
        tokenizer = AutoTokenizer.from_pretrained("gpt2")
        model = AutoModelForCausalLM.from_pretrained("gpt2")

        # Charger les données
        dataset = JSONLDataset(file_path)
        dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

        # Configurer l'optimiseur
        optimizer = AdamW(model.parameters(), lr=5e-5)

        # Entraîner le modèle
        model.train()
        for epoch in range(1):  # Une seule époque pour tester rapidement
            for batch in dataloader:
                inputs = tokenizer(batch["prompt"], return_tensors="pt", padding=True, truncation=True)
                outputs = tokenizer(batch["response"], return_tensors="pt", padding=True, truncation=True)
                labels = outputs["input_ids"]

                optimizer.zero_grad()
                loss = model(input_ids=inputs["input_ids"], labels=labels).loss
                loss.backward()
                optimizer.step()
                print(f"Loss: {loss.item()}")

        # Sauvegarder le modèle dans GCS
        output_dir = "./model"
        model.save_pretrained(output_dir)
        tokenizer.save_pretrained(output_dir)
        print(f"Modèle entraîné et sauvegardé dans {output_dir}!")

    except Exception as e:
        print(f"Erreur lors de l'entraînement : {e}")
        exit(1)

if __name__ == "__main__":
    # Chemin vers le fichier JSONL dans GCS
    data_path = "gs://gid8_training_v2/gid8_complet_training_set_v2.0.jsonl"
    print(f"Début de l'entraînement avec les données depuis : {data_path}")
    train_model(data_path)
