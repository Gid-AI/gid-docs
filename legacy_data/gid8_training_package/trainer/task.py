import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from datasets import load_dataset
import os
from google.cloud import storage

def train_model(args):
    # Charger Gemini 1.5 pro (0002) comme modèle de fondation pour GID 9
    model_id = "gemini-1.5-pro-0002"  # Remplacer par l'ID exact de Gemini 1.5 pro
    model = AutoModelForCausalLM.from_pretrained(model_id)
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    # Charger les données depuis nouveau bucket us-central1
    train_data = load_dataset(
        'json', 
        data_files='gs://gid9_training_us_central1/gid8_complet_training_set_v2.2.jsonl',
        split='train'
    )
    val_data = load_dataset(
        'json',
        data_files='gs://gid9_training_us_central1/gid9_validation_set_v1.jsonl',
        split='validation'
    )

    # Configuration avec nouveaux chemins GCS
    training_args = TrainingArguments(
        output_dir="gs://gid9_training_us_central1/gid9_output",
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        learning_rate=2e-5,
        weight_decay=0.01,
        logging_dir="gs://gid9_training_us_central1/logs",
    )

    # Préparation des données
    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True)

    tokenized_train = train_data.map(tokenize_function, batched=True)
    tokenized_val = val_data.map(tokenize_function, batched=True)

    # Entraînement
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_val,
    )

    # Lancer l'entraînement
    trainer.train()

    # Sauvegarder sur GCS
    bucket_name = "gid9_training_us_central1"
    model_path = f"gs://{bucket_name}/model"
    trainer.save_model(model_path)