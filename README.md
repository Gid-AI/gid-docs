# Gid Documentation

This repository centralizes all documentation related to Gid, serving as a comprehensive reference for architects, developers, and administrators. It provides both high-level overviews and detailed guidance on setup, coding standards, deployment strategies, and historical context.

## Contents

- **Architectural References**:  
  Includes diagrams and JSON reference files that define system behavior, data structures, trait configurations, access rules, and communication guidelines.
  - **RAG Pipeline Diagrams**: Illustrate the integration with Gemini 1.5 Pro and how documents flow through Vertex AI.
  - **Twilio Integration Flowcharts**: Show inbound/outbound message handling.
  - **Vertex AI Matching Engine Diagrams**: Depict data retrieval and semantic search logic.
  - **JSON Reference Files**:  
    - *Gid_traits_definitions.json*: Defines the 75 adjustable traits (1–10 scale) that shape Gid’s responses.  
    - *Gid_company_profiles.json*: Offers predefined trait profiles and a “Custom” option for companies.  
    - *Gid_access_rules.json*: Centralizes role-based access policies for employees, managers, and owners, plus universal rules.  
    - *Gid_guidelines.json*: Contains absolute and standard guidelines governing Gid’s communication style, tone, and adherence to company standards.

- **Developer Guides**:  
  Aiding onboarding, outlining coding standards, best practices, and recommended workflows for developing and maintaining Gid.

- **Deployment Documentation**:  
  Details environment setups, operational best practices, and CI/CD pipelines, ensuring consistent and efficient deployments.

- **Legacy_Data**:  
  Historical training data files demonstrating older formats and methodologies no longer in active use. Retained for reference and archival value.

## Directory Structure

- **architecture/**:  
  - System diagrams, flowcharts, and architectural overviews.  
  - Reference JSON files defining traits, profiles, access rules, and guidelines.  
  These materials provide a foundational understanding of how Gid’s RAG pipeline, data storage, and integration points operate.

- **dev_guides/**:  
  Developer onboarding instructions, coding conventions, style guides, and best practices. Essential reading for anyone contributing to Gid’s codebase.

- **deployment/**:  
  Instructions on deploying Gid’s backend services, configuring environments, and applying operational checklists. Useful for DevOps and release engineers.

## Usage

The documentation here is intended for quick reference and deeper comprehension. It supports:

- **Onboarding**: Helping new team members grasp system architecture, coding standards, and deployment workflows.
- **Maintenance & Scalability**: Providing developers and architects with the context needed to evolve Gid’s logic and infrastructure.
- **Compliance & Consistency**: Ensuring Gid’s responses and data access align with company policies, legal requirements, and cultural values.
