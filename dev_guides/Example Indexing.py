from google.cloud import aiplatform
import json
import glob

aiplatform.init(project="my-company-gid-project", location="us-central1")

embedding_model = aiplatform.TextEmbeddingModel("projects/my-company-gid-project/locations/us-central1/models/textembedding-gecko")

docs = glob.glob("/local_folder/policies/*.json")
all_vectors = []
for doc_path in docs:
    with open(doc_path) as f:
        doc = json.load(f)
    embedding = embedding_model.get_embeddings([doc["content"]])[0]
    all_vectors.append({"id": doc["id"], "embedding": embedding, "content": doc["content"]})

# Use the Vertex AI Matching Engine APIs to create 'gid_document_index' and upload these embeddings.
