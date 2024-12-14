import json
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import Dataset

def load_dataset(dataset_path):
    """Charge le dataset JSONL et le prépare pour l'entraînement."""
    with open(dataset_path, "r") as f:
        data = [json.loads(line) for line in f]

    # Transformer les données pour inclure ou non le contexte
    examples = []
    for item in data:
        context = item.get("context", None)  # Contexte est optionnel
        user_input = next(
            (content["parts"][0]["text"] for content in item["contents"] if content["role"] == "user"), ""
        )
        model_response = next(
            (content["parts"][0]["text"] for content in item["contents"] if content["role"] == "model"), ""
        )

        # Inclure le contexte s'il existe
        if context:
            input_text = f"Context: {context}\nUser: {user_input}\n"
        else:
            input_text = f"User: {user_input}\n"

        examples.append({
            "input": input_text,
            "output": model_response
        })

    return Dataset.from_dict({
        "input": [example["input"] for example in examples],
        "output": [example["output"] for example in examples]
    })

def main():
    # Charger les données depuis le bucket ou localement
    print("Chargement des données...")
    dataset_path = "gid8_complet_training_set_v2.0.jsonl"  # Assurez-vous que ce chemin est correct
    dataset = load_dataset(dataset_path)

    # Diviser les données en train/test
    dataset = dataset.train_test_split(test_size=0.1, seed=42)
    train_dataset = dataset["train"]
    eval_dataset = dataset["test"]

    # Charger le modèle pré-entraîné et le tokenizer
    print("Chargement du modèle et du tokenizer...")
    model_name = "gemini-1.5-pro-002"  # Exemple, à ajuster selon vos besoins
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Prétraitement des données
    def preprocess_function(examples):
        inputs = tokenizer(
            examples["input"], padding="max_length", truncation=True, max_length=512
        )
        outputs = tokenizer(
            examples["output"], padding="max_length", truncation=True, max_length=512
        )
        inputs["labels"] = outputs["input_ids"]
        return inputs

    print("Prétraitement des données...")
    tokenized_train_dataset = train_dataset.map(preprocess_function, batched=True)
    tokenized_eval_dataset = eval_dataset.map(preprocess_function, batched=True)

    # Configurer les arguments d'entraînement
    print("Configuration des arguments d'entraînement...")
    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="epoch",
        save_strategy="epoch",
        logging_dir="./logs",
        num_train_epochs=5,  # Ajustez pour plus de passes si nécessaire
        per_device_train_batch_size=4,  # Ajustez selon vos ressources
        per_device_eval_batch_size=4,
        warmup_steps=500,
        weight_decay=0.01,
        logging_steps=10,
        save_total_limit=2,
        fp16=False,  # Désactiver pour CPU
    )

    # Initialiser l'entraîneur
    print("Initialisation de l'entraîneur...")
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train_dataset,
        eval_dataset=tokenized_eval_dataset,
        tokenizer=tokenizer,
    )

    # Lancer l'entraînement
    print("Démarrage de l'entraînement...")
    trainer.train()
    print("Entraînement terminé.")

    # Sauvegarder le modèle fine-tuné
    print("Sauvegarde du modèle fine-tuné...")
    trainer.save_model("./fine_tuned_model")
    print("Modèle sauvegardé avec succès.")

if __name__ == "__main__":
    main()
