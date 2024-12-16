# Architecture

This directory provides essential architectural references, configurations, and documentation for Gid’s overall system design, data structures, and operational logic. It serves as a central point of reference for developers, architects, and administrators to understand and evolve Gid’s pipeline, data management, and behavioral guidelines.

## Overview of the RAG Pipeline and Model Integration

Gid uses a Retrieval-Augmented Generation (RAG) pipeline connected to a fine-tuned Gemini 1.5 Pro model (`gid9_tuned_model`) on Vertex AI. The pipeline:

- Loads universal guidelines, trait definitions, company profiles, and access rules from Google Cloud Storage (GCS).
- Loads enterprise-specific traits and employee histories from Firestore.
- Loads company-specific information (mission, vision, values, policies) and employee data from JSON files stored in GCS.
- Constructs a system prompt that ensures Gid’s responses align with the company’s mission, values, and globally defined guidelines and traits.
- Invokes the Vertex AI model with the enriched prompt, producing context-aware, policy-compliant answers from the first interaction.

## Key Components

### Global JSON Reference Files (in GCS)
- **Gid_guidelines.json**: Absolute and standard guidelines governing Gid’s communication style, behavior, and adherence to company standards.
- **Gid_traits_definitions.json**: Defines the 75 adjustable traits that shape Gid’s responses.
- **Gid_company_profiles.json**: Offers predefined trait profiles (e.g., "Insight_and_Growth-Oriented") plus a "Custom" option.
- **Gid_access_rules.json**: Centralizes role-based access policies for employees, managers, and owners.

These files are stored in GCS, for example:  
`gs://gid9_training_us_central1/Gid_guidelines.json`  
`gs://gid9_training_us_central1/Gid_traits_definitions.json`  
`gs://gid9_training_us_central1/Gid_company_profiles.json`  
`gs://gid9_training_us_central1/Gid_access_rules.json`

### Company-Specific Data for ABC

- **Company Data JSON**:  
  `company_data.json` consolidates mission, vision, values, policies, roles, and company-specific guidelines.  
  Stored at:  
  `gid-docs/architecture/company_info/ABC/company_data.json` (GitHub)  
  and in GCS:  
  `gs://gid9_training_us_central1/company_info/ABC/company_data.json`

- **Traits Applied to ABC**:  
  The "Insight_and_Growth-Oriented" profile from `Gid_company_profiles.json` was applied to ABC and stored in Firestore at:  
  `companies/ABC/management_traits/default_traits_document`

### Employee Histories

We have created a comprehensive employee history model and an associated schema:

- **Employee Record Schema**:  
  `gid-docs/architecture/schemas/employee_record_schema.json` defines the structure expected in employee documents.

- **Multiple Employees for ABC**:  
  A single JSON file `employee_history.json` containing 10 fictional employees, stored at:  
  `gs://gid9_training_us_central1/company_info/ABC/employee_history.json`

  Using a Python script, each employee was imported into Firestore at:  
  `companies/ABC/employee_history/{employee_id}`

### Schemas and Structuring

- **Employee Record Schema (`employee_record_schema.json`)**:  
  Provides a clear blueprint for fields and structures in an employee’s record.

### Integration Steps & Scripts

We demonstrated how to:
- Load and apply a trait profile from `Gid_company_profiles.json` to ABC in Firestore.
- Import `employee_history.json` from GCS into Firestore, creating individual documents for each employee.

### Prompt Construction and RAG Execution

With all data in place, your RAG pipeline code will:
1. Load global references (guidelines, traits, profiles, access rules) from GCS.
2. Retrieve ABC’s applied traits from Firestore.
3. Fetch ABC’s `company_data.json` from GCS.
4. Load employee-specific histories from Firestore.
5. Build a system prompt with all this context, then query the `gid9_tuned_model` on Vertex AI for aligned, context-aware answers.

### Directory Structure

- `company_info/ABC/`: Holds `company_data.json` and can hold employee JSON before Firestore import.
- `schemas/`: Holds `employee_record_schema.json`.
- Global JSON references are in GCS, but initial backups or samples can be kept here.

