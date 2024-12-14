 ```markdown
     # Gid Architecture Diagram

     The following Mermaid diagram provides a high-level, professional overview of Gid’s architecture, including user interactions, backend RAG pipeline, data sources, and infrastructure components. Once you commit this file, GitHub will automatically render the diagram below.

     ```mermaid
     flowchart LR
         %% Define styles for a professional look
         classDef title fill=#f4f4f4,stroke=#333,stroke-width=1px,color=#000,font-weight=bold,font-family=Arial
         classDef node fill=#fff,stroke=#333,stroke-width=1px,color=#000,font-family=Arial
         classDef datastore fill=#e7f3ff,stroke=#0370c0,stroke-width=1px,color=#000,font-family=Arial
         classDef service fill=#e9ffe7,stroke=#2e7d32,stroke-width=1px,color=#000,font-family=Arial
         classDef infra fill=#fff5e6,stroke=#ff9500,stroke-width=1px,color=#000,font-family=Arial

         %% Users
         U[User (Manager/Employee)]:::node

         %% Frontend/Backend
         FE[Frontend (Web Dashboard)]:::node
         T[Twilio SMS]:::node
         BE[Backend (Cloud Run - RAG Orchestrator)]:::service

         %% Vertex AI
         VAI[Vertex AI (Embeddings & Matching Engine)]:::service
         GM[Gemini 1.5 Pro Model]:::service

         %% Data Stores
         FS[(Firestore - Employee Histories)]:::datastore
         GCS[(GCS - Policies, Values, Traits)]:::datastore

         %% Infrastructure & Ops
         TF[Terraform (IaC)]:::infra
         MON[Monitoring & Dashboards]:::infra
         LG[Logging & Alerts]:::infra

         %% Flows
         U -->|SMS| T
         U -->|Web| FE
         FE -->|API Calls| BE
         T -->|HTTP POST| BE

         BE -->|Embeddings Query| VAI
         BE -->|Semantic Search| VAI
         BE -->|Prompt| GM
         GM -->|Response| BE

         BE -->|Read/Write| FS
         BE -->|Fetch Docs| GCS

         BE -->|Send Response| T
         BE -->|Update Frontend| FE

         %% Infra relations (not actual calls, just conceptual)
         TF -.-> BE
         TF -.-> FS
         TF -.-> GCS
         TF -.-> VAI
         MON -.-> BE
         MON -.-> FE
         LG -.-> BE

         %% Titles or grouping
         class U,FE,T,BE,VAI,GM,FS,GCS,TF,MON,LG node
     ```
     
