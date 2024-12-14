# README: Setting up Gid with RAG, Gemini 1.5 Pro, Google Cloud, and Twilio

## Overview
This document provides a detailed step-by-step guide to implement Gid, an AI assistant using Retrieval-Augmented Generation (RAG) with the Gemini 1.5 Pro foundation model on Google Cloud. Gid will always reference your company’s mission, vision, values, policies, management traits, and the full employee history in each interaction. Communication will occur primarily via Twilio (SMS), as well as web and email. All resource names and instructions provided here should be followed exactly without modification.

## Architecture Summary
1. The employee or manager sends a message to Gid via Twilio SMS (or web/email).
2. Twilio forwards the request to a backend API hosted on Google Cloud (Cloud Run).
3. The backend executes a RAG pipeline:
   - Uses embeddings and Vertex AI Matching Engine to retrieve relevant documents (policies, employee history, traits).
   - Constructs a context-rich prompt and sends it to the Gemini 1.5 Pro model on Vertex AI.
4. The model responds, and the response is sent back to the user via Twilio.
5. The employee’s history is updated in Firestore after each interaction, ensuring Gid has a holistic and continually updated view.

## Google Cloud Components
- **Project**: Create a GCP project named `my-company-gid-project`.
- **Vertex AI**:
  - Use the Gemini 1.5 Pro model: `projects/my-company-gid-project/locations/us-central1/models/gemini-1_5-pro`.
  - Use Vertex AI Embeddings for embedding user queries and documents.
  - Use Vertex AI Matching Engine for the vector store to store and retrieve embeddings.
- **Google Cloud Storage (GCS)**:
  - Create a GCS bucket named `my-company-gid-docs` in `us-central1`.
  - Store company documents (policies, mission, vision, values) in this bucket.
    - `gs://my-company-gid-docs/policies/` for JSON policy files.
    - `gs://my-company-gid-docs/company_info/mission.json`
    - `gs://my-company-gid-docs/company_info/vision.json`
    - `gs://my-company-gid-docs/company_info/values.json`
- **Firestore**:
  - Use Firestore in Native mode.
  - Create a collection `employee_history` for storing employee profiles and interaction history.
  - Create a collection `management_traits` to store the 75 management traits.
- **Cloud Run**:
  - Deploy a backend service named `gid-backend` in `us-central1`.
- **Secret Manager**:
  - Store Twilio credentials as `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN`.
- **IAM**:
  - Assign minimal necessary IAM roles to the Cloud Run service account (access to Firestore, Secret Manager, Vertex AI, Storage).

## Data Structures
### Company Documents Format (Policies)
Store policies in `gs://my-company-gid-docs/policies/` as JSON files, for example `telework_policy.json`:
```json
{
  "id": "doc-telework-policy",
  "title": "Telework Policy",
  "content": "Employees are allowed to work remotely under the following conditions...",
  "metadata": {
    "category": "policy",
    "effective_date": "2024-01-01",
    "company": "MyCompany"
  }
}


##  RAG Pipeline Steps
Identify Employee: Determine the employee ID from the incoming phone number (Twilio) or other user identifier.
Load Employee History: Fetch from employee_history to get their profile and past interactions.
Load Company Info & Traits: Fetch mission.json, vision.json, values.json from GCS and default_traits_document from management_traits.
Generate User Query Embedding: Use Vertex AI Embeddings to embed the user’s incoming message.
Retrieve Relevant Docs: Query Vertex AI Matching Engine to find policies and other documents most relevant to the query.
Construct Prompt: Combine mission, vision, values, relevant docs, employee history, and traits into a well-structured prompt.
Call Gemini 1.5 Pro: Send the prompt to the model and get the response.
Update and Return: Send the generated response back to the user and update employee_history with the new interaction.
Setting up the Embeddings and Vector Index
Download documents from gs://my-company-gid-docs/.
Use Vertex AI Embeddings to generate embeddings for each document’s content.
Create a Vertex AI Matching Engine index named gid_document_index and upload the embeddings.
Ensure the Cloud Run service account has access to query the index.

## Backend (Cloud Run) Implementation
Implement a Python backend (e.g., Flask or FastAPI).
Handle Twilio incoming requests at /twilio_webhook.
On receiving a message:
Identify the employee.
Fetch employee history from employee_history.
Fetch traits and company info.
Generate embeddings for the user message.
Query the vector store (Matching Engine) for relevant docs.
Build the prompt and call Gemini 1.5 Pro.
Update employee_history with the new interaction.
Respond via Twilio.


Twilio Integration
Purchase a Twilio phone number.
In the Twilio console, set the SMS webhook URL to your Cloud Run endpoint, e.g. https://gid-backend-xyz.run.app/twilio_webhook.
Make sure TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN are stored in Secret Manager and that your application fetches them at runtime.
Every SMS sent to the Twilio number triggers a POST request to the /twilio_webhook endpoint. The backend processes the request, uses the RAG pipeline, and sends back a Twilio-compatible response.
Security, Compliance, and Updates
Use IAM to grant the Cloud Run service only the necessary roles (roles/aiplatform.user, roles/storage.objectViewer, roles/datastore.user, roles/secretmanager.secretAccessor).
Keep Twilio credentials in Secret Manager, not in code.
When policies or company info change, update gs://my-company-gid-docs/ with the new files, regenerate embeddings, and update the Matching Engine index.
Firestore will automatically track new interactions.
References
Vertex AI Docs: https://cloud.google.com/vertex-ai/docs
Vertex AI Matching Engine: https://cloud.google.com/vertex-ai/docs/matching-engine
Firestore: https://cloud.google.com/firestore/docs
Twilio SMS API: https://www.twilio.com/docs/sms
Following these instructions exactly should result in a fully operational RAG-based Gid assistant integrated with Gemini 1.5 Pro on Google Cloud and Twilio SMS.



