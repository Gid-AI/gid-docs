from google.cloud import aiplatform

# Initialiser Vertex AI
aiplatform.init(
    project="gid-ai-5",
    location="northamerica-northeast1",
)

# ID du modèle pré-entraîné comme base
base_model = "projects/gid-ai-5/locations/northamerica-northeast1/models/5694933670205325312"

# Paramètres d'entraînement
training_pipeline = aiplatform.CustomTrainingJob(
    display_name="gid-text-generation-training",
    script_path=None,  # Pas de script personnalisé pour cette itération simple
    container_uri="us-docker.pkg.dev/vertex-ai/training/tf-gpu.2-11:latest",  # Conteneur GPU par défaut
    model_serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-11:latest",
)

# Lancer le fine-tuning
model = training_pipeline.run(
    dataset="gs://gid8_training_v2/gid8_complet_training_set_v2.0.jsonl",
    model_display_name="gid8_fine_tuned_v2",
    base_model=base_model,  # Modèle existant comme base
)

print(f"Modèle fine-tuné et disponible : {model.resource_name}")
