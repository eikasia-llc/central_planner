# Master Plan: Intelligent Control SaaS
- status: active
- type: plan
- id: master_plan.saas
- owner: product-manager
- priority: critical
- last_checked: 2026-01-23T15:14:25+01:00
<!-- content -->
This document serves as the central strategic plan for the **Intelligent Control & Analysis Platform**. It is a dual-engine AI system functioning as both a **Business Analyst** and an **Autonomous Operator** for SMBs and industrial clients. It combines LLM reasoning (Analysis) with RL control (Optimization).

## Executive Summary
- status: done
- type: context
- id: product.saas.summary
- last_checked: 2026-01-23T13:47:07+01:00
<!-- content -->
**The Vision**: Transform data into decision. The platform allows clients to "chat with data" and optimize operations using a conversational interface backed by rigorous execution engines.
-   **Analyst**: "Why is this happening?" -> Code Interpreter analysis.
-   **Controller**: "Optimize for efficiency." -> RL Agent execution.

**Value Propositions**
1.  **Retail/SMBs (The Agentic Analyst)**: Democratized Data Science. Instant answers to colloquial questions without a data team.
2.  **Logistics (Inventory Auto-Pilot)**: Cash flow optimization. Automated reordering using RL agents to solve the Newsvendor problem (minimize holding costs vs. prevent stockouts).

## Technical Architecture
- status: active
- type: plan
- id: product.saas.arch
- last_checked: 2026-01-23T13:47:07+01:00
<!-- content -->
The system separates Analytical Queries (Code Execution) from Control Tasks (Model Inference).

### Core Components
- status: active
- type: context
- id: product.saas.arch.components
- last_checked: 2026-01-23T13:47:07+01:00
<!-- content -->
-   **Chatbot Assistant App**: Interface with the user, operating also as a data warehouse.
-   **Internal Ecosystem of AI-Assistants**: Background agents performing different tasks, well orchestrated (internal access only).
-   **BigQuery Database**: Google BigQuery (or alternative) for data storage.
-   **Cloud Compute**: Google Cloud or other platform for computation.
-   **Internal Algorithms Repository**: Data processing and control algorithms, leveraging Vertex AI for data science and optimization.

### Information Flow
- status: active
- type: context
- id: product.saas.arch.flow
- last_checked: 2026-01-23T13:47:07+01:00
<!-- content -->

#### AI Assistant Orchestration
- status: active
- type: context
- id: product.saas.arch.flow.orchestration
- last_checked: 2026-01-23T15:28:59+01:00
<!-- content -->
User interaction begins with the Chatbot App, which forwards requests to the Orchestrator (Vertex AI).
1.  **Intent Recognition**: The Orchestrator determines if the request is **Analysis** (informational) or **Control** (actionable).
2.  **Routing**:
    *   **Analysis**: Routed to Code Interpreter / Analyst Agent for data querying and visualization.
    *   **Control**: Routed to Planner / RL Agent for optimization and decision making.
3.  **Response**: Results are aggregated and returned to the Chatbot as natural language or UI components.

#### Control Loop
- status: active
- type: context
- id: product.saas.arch.flow.control
- last_checked: 2026-01-23T15:28:59+01:00
<!-- content -->
This high-frequency loop handles the autonomous optimization system:
1.  **Telemetry Ingest**: Raw data streams from the Client App/Warehouse are ingested into BigQuery.
2.  **State Estimation**: Processing algorithms convert raw telemetry into state vectors ($s_t$) suitable for model input.
3.  **Decision**: The Policy network ($\pi$) or Planer selects the optimal action ($a_t$) based on the current state.
4.  **Execution & Feedback**: The action is sent to the Controller for execution, and the outcome is recorded for offline re-training and refinement.

## Implementation Roadmap
- status: active
- type: plan
- id: product.saas.roadmap
- last_checked: 2026-01-23T13:47:07+01:00
<!-- content -->

### Phase 1: Unified Data API
- status: todo
- type: task
- id: product.saas.roadmap.phase1
- estimate: 2w
- last_checked: 2026-01-23T13:47:07+01:00
<!-- content -->
**Goal**: Single API surface for uploading both Event data (Recs) and Telemetry (Control).
**Deliverables**:
-   Robust Ingestion Layer.
-   Schema validation via Pydantic.
-   Endpoints: `/v1/events` (to BigQuery) and `/v1/telemetry` (to BigQuery/BigTable).

#### Basic Chatbot Interface
- status: todo
- type: task
- id: product.saas.roadmap.phase1.chatbot
- estimate: 1w
- last_checked: 2026-01-23T15:11:55+01:00
<!-- content -->
Create a basic chat interface to interact with the LLMs. This involves setting up a simple React UI, establishing the API connection to Vertex AI / OpenAI, and implementing basic cost tracking per session.

#### Client Data Warehouse App
- status: todo
- type: task
- id: product.saas.roadmap.phase1.warehouse_app
- blocked_by: [product.saas.roadmap.phase1.chatbot]
- estimate: 1w
- last_checked: 2026-01-23T14:48:58+01:00
<!-- content -->
Develop a downloadable application for clients to install, enabling streamlined data streaming to our central warehouse.

#### Data Stream Controllers & Planners
- status: todo
- type: task
- id: product.saas.roadmap.phase1.controllers
- blocked_by: [product.saas.roadmap.phase1.warehouse_app]
- estimate: 1w
- last_checked: 2026-01-23T14:48:58+01:00
<!-- content -->
Set up initial controllers and planners to process the incoming data stream from the client app.

### Phase 2: The Agentic Analyst (Generative UI)
- status: todo
- type: task
- id: product.saas.roadmap.phase2
- blocked_by: [product.saas.roadmap.phase1]
- estimate: 4w
- last_checked: 2026-01-23T13:47:07+01:00
<!-- content -->
**Goal**: Enable "Chat with Data" with interactive components (React).
**Actions**:
-   **Frontend**: Build Component Registry (Charts, Tables, Sliders).
-   **Backend**: Implement tool_call logic in Vertex AI to map requests to UI JSON payloads.
-   **Prompting**: Train model to prefer returning UI components over dense text.

### Phase 3: The Control Loop (MVP)
- status: todo
- type: task
- id: product.saas.roadmap.phase3
- blocked_by: [product.saas.roadmap.phase2]
- estimate: 6w
- last_checked: 2026-01-23T13:47:07+01:00
<!-- content -->
**Goal**: End-to-end RL pipeline.
**Actions**:
-   Implement standard algorithm (e.g., PPO) on Vertex Custom Jobs.
-   Train on a simple inventory management problem (Environment).

## Security & Safety Checks
- status: active
- type: guideline
- id: product.saas.security
- last_checked: 2026-01-23T13:47:07+01:00
<!-- content -->
-   **Indirect Execution**: Clients only submit natural language, never code.
-   **Repository Scoping**: Generated code can only import whitelisted libraries (`pandas`, `numpy`, `lib_analysis`). No `os` or `sys`.
-   **Simulation Isolation**: User-provided logic runs in `gVisor` sandboxes.
-   **Action Bounding**: Deterministic logic layer validates actions against safety constraints (e.g., `MAX_ORDER_LIMIT`) before execution.

## Research Directions
- status: active
- type: plan
- id: product.saas.research
- last_checked: 2026-01-23T13:47:07+01:00
<!-- content -->
-   **MBRL (DreamerV3)**: Learning World Models from telemetry to simulate environments.
-   **Safe RL**: Constrained MDPs (Lagrangian Relaxation) to ensure safety during exploration.
-   **Reflexion**: Agents that analyze their own tracebacks to iteratively fix code.
