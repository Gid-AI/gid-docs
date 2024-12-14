import os
from datetime import datetime
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from google.cloud import firestore
from google.cloud import aiplatform

# Initialize Firestore
db = firestore.Client(project="my-company-gid-project")

app = Flask(__name__)

def get_employee_id_from_phone(phone_number):
    # Implement logic or store a mapping in Firestore to map phone_number -> employee_id
    # For this example, return a known employee_id.
    return "EMPLOYEE_001"

def get_employee_data(employee_id):
    doc_ref = db.collection("employee_history").document(employee_id)
    return doc_ref.get().to_dict()

def get_management_traits():
    doc_ref = db.collection("management_traits").document("default_traits_document")
    return doc_ref.get().to_dict()

def load_company_mission():
    # Download mission.json from GCS and return content
    return "Our mission is to elevate organizational dynamics and sustainable success."

def load_company_vision():
    # Download vision.json from GCS
    return "Our vision is to foster continuous improvement and meaningful collaboration."

def load_company_values():
    # Download values.json from GCS
    return "Respect, Integrity, Innovation."

def summarize_interactions(interactions):
    # Summarize last few interactions. Here, a simple placeholder.
    return "Summarized recent employee interactions."

def get_user_query_embedding(query):
    # Call Vertex AI Embeddings API
    # This is a placeholder. In reality, you'd use aiplatform.TextEmbeddingModel:
    # embedding_model = aiplatform.TextEmbeddingModel(...)
    # embedding = embedding_model.get_embeddings([query])[0]
    return [0.1, 0.2, 0.3]

def query_vector_store(embedding):
    # Query Matching Engine using embedding to get relevant documents
    # Placeholder: return a sample doc
    return [{
        "title": "Telework Policy",
        "content": "Employees may work remotely if they meet certain criteria..."
    }]

def build_prompt(employee_data, relevant_docs, traits, user_message, mission, vision, values):
    trait_names = ", ".join([t["name"] for t in traits["traits"]])
    docs_text = "".join([doc["title"] + ": " + doc["content"] + "\n" for doc in relevant_docs])

    prompt = f"""
Mission: {mission}
Vision: {vision}
Values: {values}

Employee: {employee_data["profile"]["name"]}, Role: {employee_data["profile"]["role"]}
Recent History: {summarize_interactions(employee_data["interactions"])}
Management Traits: {trait_names}

Relevant Documents:
{docs_text}

User: {user_message}
Please provide a clear, contextually informed response.
"""
    return prompt

def call_gemini_model(prompt):
    # Call Gemini 1.5 Pro Model via Vertex AI
    # aiplatform.init(...)
    # llm = aiplatform.TextGenerationModel(...)
    # response = llm.predict(prompt=prompt, temperature=0.2, max_output_tokens=1024)
    # return response.text
    return "Generated response from Gemini 1.5 Pro"

def update_employee_history(employee_id, request_msg, response_msg, relevant_docs):
    doc_ref = db.collection("employee_history").document(employee_id)
    current = doc_ref.get().to_dict()
    interactions = current.get("interactions", [])
    interactions.append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "request": request_msg,
        "response": response_msg,
        "context_used": [doc["title"] for doc in relevant_docs]
    })
    doc_ref.update({"interactions": interactions})

def process_user_message(employee_id, user_message):
    employee_data = get_employee_data(employee_id)
    traits = get_management_traits()
    mission = load_company_mission()
    vision = load_company_vision()
    values = load_company_values()
    user_embedding = get_user_query_embedding(user_message)
    relevant_docs = query_vector_store(user_embedding)
    prompt = build_prompt(employee_data, relevant_docs, traits, user_message, mission, vision, values)
    response = call_gemini_model(prompt)
    update_employee_history(employee_id, user_message, response, relevant_docs)
    return response

@app.route("/twilio_webhook", methods=["POST"])
def twilio_webhook():
    from_number = request.form.get("From")
    message_body = request.form.get("Body")
    employee_id = get_employee_id_from_phone(from_number)
    response_text = process_user_message(employee_id, message_body)
    resp = MessagingResponse()
    resp.message(response_text)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
