# README: Multi-Company Setup Firestore

This document provides a comprehensive guide to configuring Gid as a multi-tenant solution, allowing each client company to have its own mission, vision, values, policies, procedures, and management trait adjustments. By organizing data and indexes per company, Gid can adapt responses to each organization’s unique context.

## Key Principles of Multi-Tenancy

1. Identify the Company:  
   When an employee sends a message via Twilio (or other channels), determine the `company_id` from their `employee_id` (e.g., by mapping their phone number to their employee and company). For example, have a Firestore collection `phone_to_employee` that maps `phone_number` -> `{employee_id, company_id}`.

2. Per-Company Data Storage:  
   Instead of storing all data globally, create separate namespaces for each company’s data.

   Example Firestore structure:
   
       companies
         └── {company_id}
              ├── employee_history
              │    └── {employee_id}
              ├── management_traits
              │    └── default_traits_document
              └── other company-specific collections

   Example GCS structure:
   
       gs://my-company-gid-docs/{company_id}/policies/*.json
       gs://my-company-gid-docs/{company_id}/company_info/mission.json
       gs://my-company-gid-docs/{company_id}/company_info/vision.json
       gs://my-company-gid-docs/{company_id}/company_info/values.json

   Each company has its own directory and Firestore subtree.

3. Embeddings and Matching Engine per Company:  
   When indexing documents for the Vertex AI Matching Engine, include a `company_id` field in the metadata. During queries, filter results to only return documents for the correct `company_id`.

## Adjusting the RAG Pipeline for Multi-Tenancy

1. Upon receiving a message (SMS from Twilio), identify the `company_id` and `employee_id`:
   
       company_id, employee_id = get_company_and_employee_id_by_phone(phone_number)

2. Load company-specific data:
   
   - Employee history from Firestore:
     
         companies/{company_id}/employee_history/{employee_id}

   - Management traits:
     
         companies/{company_id}/management_traits/default_traits_document

   - Mission, vision, values:
     
         gs://my-company-gid-docs/{company_id}/company_info/mission.json
         gs://my-company-gid-docs/{company_id}/company_info/vision.json
         gs://my-company-gid-docs/{company_id}/company_info/values.json

   - Policies:
     
         gs://my-company-gid-docs/{company_id}/policies/*.json

3. On indexing documents, add the `company_id` to metadata so that the Matching Engine queries can filter by `company_id`.

   For example, when indexing a document:
   
       {
         "id": doc["id"],
         "embedding": embedding,
         "content": doc["content"],
         "metadata": {
             "company_id": company_id,
             "category": doc["metadata"]["category"]
         }
       }

4. Querying the Vector Store with a filter by `company_id`:
   
   After obtaining results from the Matching Engine, filter them:
   
       filtered_results = [r for r in results if r.metadata["company_id"] == company_id]

5. Construct the prompt using only the data for the identified `company_id`, ensuring the mission, vision, values, traits, and policies match that company.

6. Call the Gemini 1.5 Pro model with the company-specific prompt and documents.

7. Update the employee’s history under `companies/{company_id}/employee_history/{employee_id}`.

## Example Code Flow

    def process_user_message(phone_number, user_message):
        # Identify the company and employee
        company_id, employee_id = get_company_and_employee_id_by_phone(phone_number)

        # Load company-specific data
        employee_data = get_employee_data(company_id, employee_id)
        traits = get_management_traits(company_id)
        mission = load_company_mission(company_id)
        vision = load_company_vision(company_id)
        values = load_company_values(company_id)

        # Embed user message
        user_embedding = get_user_query_embedding(user_message)

        # Query vector store for this company only
        relevant_docs = query_vector_store(user_embedding, company_id)

        # Build prompt with company-specific context
        prompt = build_prompt(employee_data, relevant_docs, traits, user_message, mission, vision, values)

        # Call the Gemini 1.5 Pro model
        response = call_gemini_model(prompt)

        # Update the employee history for this company
        update_employee_history(company_id, employee_id, user_message, response, relevant_docs)

        # Return the response
        return response

## Advantages of this Approach

- Data Isolation: Each company’s data is stored separately, ensuring no cross-contamination of contexts.
- Easier Maintenance: Updating an individual company’s policies or values does not affect other clients.
- Scalability: Easily onboard new companies by creating their own `company_id` namespaces without impacting existing customers.

## Security and Access Control

- Use IAM and Firestore security rules to ensure that each company’s data can only be accessed by authorized code paths.
- Keep sensitive credentials in Secret Manager.
- Apply the same security best practices as in a single-tenant environment, but repeated for each company namespace.

## Conclusion

By organizing data, embeddings, and references by `company_id`, you create a fully multi-tenant version of Gid. This allows Gid to provide a unique and contextually appropriate experience for each company it serves, integrating seamlessly with Gemini 1.5 Pro, Vertex AI, Firestore, GCS, and Twilio.
