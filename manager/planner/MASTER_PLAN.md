# Central Company Master Plan
- status: active
- type: plan
- id: master_plan
- owner: central-planner
- last_checked: 2026-01-23T13:47:07+01:00
<!-- content -->
This document serves as the central aggregation point for the company's strategic initiatives. It currently focuses on the flagship **Intelligent Control & Analysis Platform**.

## Intelligent Control & Analysis Platform (SaaS)
- status: active
- type: plan
- id: product.saas
- owner: product-manager
- priority: critical
- last_checked: 2026-01-23T13:47:07+01:00
<!-- content -->
A dual-engine AI system functioning as both a **Business Analyst** and an **Autonomous Operator** for SMBs and industrial clients. It combines LLM reasoning (Analysis) with RL control (Optimization).

### Executive Summary
- status: done
- type: context
- id: product.saas.summary
- last_checked: 2026-01-23T13:47:07+01:00
<!-- content -->
**The Vision**: Transform data into decision. The platform allows clients to "chat with data" and optimize operations using a conversational interface backed by rigorous execution engines.
-   **Analyst**: "Why is this happening?" -> Code Interpreter analysis.
-   **Controller**: "Optimize for efficiency." -> RL Agent execution.

### Value Propositions
- status: active
- type: context
- id: product.saas.value_prop
- last_checked: 2026-01-23T13:47:07+01:00
<!-- content -->
1.  **Retail/SMBs (The Agentic Analyst)**: Democratized Data Science. Instant answers to colloquial questions without a data team.
2.  **Logistics (Inventory Auto-Pilot)**: Cash flow optimization. Automated reordering using RL agents to solve the Newsvendor problem (minimize holding costs vs. prevent stockouts).

### Technical Architecture
- status: active
- type: plan
- id: product.saas.arch
- last_checked: 2026-01-23T13:47:07+01:00
<!-- content -->
The system separates Analytical Queries (Code Execution) from Control Tasks (Model Inference).

#### Core Components
- status: active
- type: context
- id: product.saas.arch.components
- last_checked: 2026-01-23T13:47:07+01:00
<!-- content -->
-   **Orchestrator (The Brain)**: Vertex AI (Gemini Pro). Routes requests to Analysis or Control.
-   **Analysis Sandbox**: Ephemeral Docker Containers (E2B / Vertex Extensions) for safe code execution. Internal access only.
-   **Control Factory**: Vertex AI Custom Training + Ray/Stable Baselines3 for training RL policies.

#### Information Flow (Control Loop)
- status: active
- type: context
- id: product.saas.arch.flow
- last_checked: 2026-01-23T13:47:07+01:00
<!-- content -->
1.  **Input**: Client streams telemetry ($s_t$) to `/v1/telemetry`.
2.  **Inference**: Policy network $\pi(s_t)$ or World Model $\hat{f}(s, a)$ selects action.
3.  **Action**: API returns action $a_t$.
4.  **Feedback**: Client sends reward/new state during offline retraining.

### Implementation Roadmap
- status: active
- type: plan
- id: product.saas.roadmap
- last_checked: 2026-01-23T13:47:07+01:00
<!-- content -->

#### Phase 1: Unified Data API
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

##### Basic Chatbot Interface
- status: todo
- type: task
- id: product.saas.roadmap.phase1.chatbot
- estimate: 1w
- last_checked: 2026-01-23T15:11:55+01:00
<!-- content -->
Create a basic chat interface to interact with the LLMs. This involves setting up a simple React UI, establishing the API connection to Vertex AI / OpenAI, and implementing basic cost tracking per session.

##### Client Data Warehouse App
- status: todo
- type: task
- id: product.saas.roadmap.phase1.warehouse_app
- blocked_by: [product.saas.roadmap.phase1.chatbot]
- estimate: 1w
- last_checked: 2026-01-23T14:48:58+01:00
<!-- content -->
Develop a downloadable application for clients to install, enabling streamlined data streaming to our central warehouse.

##### Data Stream Controllers & Planners
- status: todo
- type: task
- id: product.saas.roadmap.phase1.controllers
- blocked_by: [product.saas.roadmap.phase1.warehouse_app]
- estimate: 1w
- last_checked: 2026-01-23T14:48:58+01:00
<!-- content -->
Set up initial controllers and planners to process the incoming data stream from the client app.

#### Phase 2: The Agentic Analyst (Generative UI)
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

#### Phase 3: The Control Loop (MVP)
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

### Security & Safety Checks
- status: active
- type: guideline
- id: product.saas.security
- last_checked: 2026-01-23T13:47:07+01:00
<!-- content -->
-   **Indirect Execution**: Clients only submit natural language, never code.
-   **Repository Scoping**: Generated code can only import whitelisted libraries (`pandas`, `numpy`, `lib_analysis`). No `os` or `sys`.
-   **Simulation Isolation**: User-provided logic runs in `gVisor` sandboxes.
-   **Action Bounding**: Deterministic logic layer validates actions against safety constraints (e.g., `MAX_ORDER_LIMIT`) before execution.

### Research Directions
- status: active
- type: plan
- id: product.saas.research
- last_checked: 2026-01-23T13:47:07+01:00
<!-- content -->
-   **MBRL (DreamerV3)**: Learning World Models from telemetry to simulate environments.
-   **Safe RL**: Constrained MDPs (Lagrangian Relaxation) to ensure safety during exploration.
-   **Reflexion**: Agents that analyze their own tracebacks to iteratively fix code.

## Repository Maintenance
- status: active
- type: recurring
- id: meta.maintenance
- last_checked: 2026-01-23T13:47:07+01:00
<!-- content -->
To sync this plan with other repositories, run:
`python3 manager/update_master_plan.py --all`
