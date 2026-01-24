# Master Plan: Intelligent Control SaaS
- status: active
- type: plan
- id: master_plan.saas
- owner: product-manager
- priority: critical
- context_dependencies: { "manager": "MANAGER_AGENT.md", "conventions": "../../MD_CONVENTIONS.md" }
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
#### Chatbot Assistant App
- status: active
- type: context
- id: product.saas.arch.components.chatbot
- last_checked: 2026-01-23T19:47:31+01:00
<!-- content -->
Serves as the primary interface for users, functioning simultaneously as a mechanism for interaction and a local data warehouse. It facilitates data collection and user intent capture.

#### Internal Ecosystem of AI-Assistants
- status: active
- type: context
- id: product.saas.arch.components.ecosystem
- last_checked: 2026-01-23T19:47:31+01:00
<!-- content -->
A background orchestration layer where multiple specialized AI agents collaborate. These agents are internal-only and handle specific sub-tasks to ensure seamless system operation.

#### Cloud Infrastructure (BigQuery & Compute)
- status: active
- type: context
- id: product.saas.arch.components.cloud
- last_checked: 2026-01-23T19:47:31+01:00
<!-- content -->
The scalable backbone of the platform. It includes **Google BigQuery** for massive data warehousing and **Google Cloud Compute** for performant processing, ensuring reliability and speed.

#### Internal Algorithms Repository
- status: active
- type: context
- id: product.saas.arch.components.algorithms
- last_checked: 2026-01-23T19:47:31+01:00
<!-- content -->
The central library of data processing and control algorithms. This leverages **Vertex AI** for advanced data science modeling and optimization tasks, representing the core intellectual property of the analysis engine.

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

#### Human-AI Interaction
- status: active
- type: context
- id: product.saas.arch.flow.human_ai
- last_checked: 2026-01-23T19:51:07+01:00
<!-- content -->
Defines the protocols for how humans interact with the AI agents.

##### Developer-AI Interaction
- status: active
- type: protocol
- id: product.saas.arch.flow.human_ai.developer
- last_checked: 2026-01-23T19:51:07+01:00
<!-- content -->
Protocol for developers to configure, train, and debug agents. Involves direct access to internal logs, model weights, and the 'Analysis Sandbox' for safe code testing.

##### Client-AI Interaction
- status: active
- type: protocol
- id: product.saas.arch.flow.human_ai.client
- last_checked: 2026-01-23T19:51:07+01:00
<!-- content -->
Protocol for end-users. Restricted to natural language via the Chatbot App. No direct code execution allowed. Intent is parsed by the Orchestrator.

#### AI-Tools Protocols
- status: active
- type: protocol
- id: product.saas.arch.flow.tools
- last_checked: 2026-01-23T19:51:07+01:00
<!-- content -->
Protocols for how AI agents utilize external software and APIs. Adheres to the **Model Context Protocol (MCP)** to standardize tool definition, discovery, and execution.


### Knowledge Bases
- status: active
- type: context
- id: product.saas.arch.knowledge
- last_checked: 2026-01-23T20:00:00+01:00
<!-- content -->
Repository resources categorized by their function.

#### Agentic
- status: active
- type: context
- id: product.saas.arch.knowledge.agentic
- last_checked: 2026-01-23T20:00:00+01:00
<!-- content -->
- [MANAGER_AGENT](MANAGER_AGENT.md)
- [CLEANER_AGENT](../cleaner/CLEANER_AGENT.md)
- [REACT_ASSISTANT](../../AI_AGENTS/specialists/REACT_ASSISTANT.md)
- [RECSYS_AGENT](../../AI_AGENTS/specialists/RECSYS_AGENT.md)
- [CONTROL_AGENT](../../AI_AGENTS/specialists/CONTROL_AGENT.md)
- [UI_DESIG_ASSISTANT](../../AI_AGENTS/specialists/UI_DESIG_ASSISTANT.md)
- [LINEARIZE_AGENT](../../AI_AGENTS/specialists/LINEARIZE_AGENT.md)
- [MC_AGENT](../../AI_AGENTS/specialists/MC_AGENT.md)

#### Knowledge
- status: active
- type: context
- id: product.saas.arch.knowledge.general
- last_checked: 2026-01-23T20:00:00+01:00
<!-- content -->
- [README](../../README.md)
- [MD_CONVENTIONS](../../MD_CONVENTIONS.md)
- [AGENTS](../../AGENTS.md)
- [AGENTS_LOG](../../AGENTS_LOG.md)
- [DAG_Example](../../language/example/DAG_Example.md)

## Implementation Roadmap
- status: active
- type: plan
- id: product.saas.roadmap
- last_checked: 2026-01-23T21:44:23+01:00
<!-- content -->
This roadmap strips away enterprise complexity to focus on the core value proposition: a local app that acts as a data hub and a chat interface, connected to powerful cloud agents for execution.

### Phase 1: The Local Nexus (Client App)
- status: todo
- type: plan
- id: product.saas.roadmap.phase1
- estimate: 4w
- last_checked: 2026-01-23T21:44:23+01:00
<!-- content -->
**Objective**: Build the interface that serves as both the chatbot and the local data warehouse.

#### Local Chat Interface
- status: todo
- type: task
- id: product.saas.roadmap.phase1.chat_ui
- estimate: 2w
- last_checked: 2026-01-23T21:44:23+01:00
<!-- content -->
- **Tech**: Electron (React) or Streamlit for a unified desktop feel.
- **Features**:
  - Chat window for natural language query.
  - "Upload Data" button (CSV/Excel).
  - Rendering engine for Tables and Charts returned by the cloud.

#### Local Data Warehouse Engine
- status: todo
- type: task
- id: product.saas.roadmap.phase1.local_db
- blocked_by: [product.saas.roadmap.phase1.chat_ui]
- estimate: 2w
- last_checked: 2026-01-23T21:44:23+01:00
<!-- content -->
- **Tech**: SQLite or DuckDB (embedded OLAP).
- **Function**:
  - Ingest user files into a structured SQL format locally.
  - Allow the app to query itself for basic stats without hitting the cloud.
  - **Change Tracking**: Automatically flag new or modified records to trigger the autonomous cloud sync.

### Phase 2: The Cloud Bridge (Connectivity)
- status: todo
- type: plan
- id: product.saas.roadmap.phase2
- blocked_by: [product.saas.roadmap.phase1]
- estimate: 2w
- last_checked: 2026-01-23T21:44:23+01:00
<!-- content -->
**Objective**: Establish a secure, simple pipe between the Local Node and the Cloud Agents.

#### API Gateway & Auth
- status: todo
- type: task
- id: product.saas.roadmap.phase2.api
- estimate: 1w
- last_checked: 2026-01-23T21:44:23+01:00
<!-- content -->
- **Tech**: Google Cloud Run (Serverless) + FastAPI.
- **Auth**: Simple API Key or Firebase Auth to link a specific Local Node to its Cloud resources.
- **Endpoints**:
  - `/agent/analyze`: Sends user query + relevant data snippets.
  - `/agent/optimize`: Sends telemetry for RL processing.

#### Autonomous Data Sync Pipeline
- status: todo
- type: task
- id: product.saas.roadmap.phase2.sync
- blocked_by: [product.saas.roadmap.phase2.api]
- estimate: 1w
- last_checked: 2026-01-23T21:44:23+01:00
<!-- content -->
- **Mechanism**: A background service in the Local App autonomously synchronizes the local warehouse with the Cloud Database.
- **Efficiency**: Pushes delta updates (only changes) to Cloud Storage/BigQuery to minimize bandwidth.
- **Policy**: Real-time sync for active telemetry; scheduled sync for large historical datasets.

### Phase 3: The Cloud Agents (Execution)
- status: todo
- type: plan
- id: product.saas.roadmap.phase3
- blocked_by: [product.saas.roadmap.phase2]
- estimate: 6w
- last_checked: 2026-01-23T21:44:23+01:00
<!-- content -->
**Objective**: The "Brain" that runs code and retrieves information.

#### Agent Orchestrator
- status: todo
- type: task
- id: product.saas.roadmap.phase3.orchestrator
- estimate: 2w
- last_checked: 2026-01-23T21:44:23+01:00
<!-- content -->
- **Tech**: LangChain or Vertex AI Agent Builder.
- **Role**:
  - Receive user text.
  - Decide: "Do I need to write code?" (Analyst) or "Do I need to run an optimization?" (Controller).
  - Route the request.

#### The Analyst Agent (Code Interpreter)
- status: todo
- type: task
- id: product.saas.roadmap.phase3.analyst
- blocked_by: [product.saas.roadmap.phase3.orchestrator]
- estimate: 2w
- last_checked: 2026-01-23T21:44:23+01:00
<!-- content -->
- **Sandbox**: Secure Python environment (e.g., E2B or restricted Docker container).
- **Workflow**:
  1. Agent writes Python code to analyze the uploaded data.
  2. Executes code.
  3. Captures output (Text + Image/JSON for charts).
  4. Returns structured response to Local App.

#### The Controller Agent (Optimization)
- status: todo
- type: task
- id: product.saas.roadmap.phase3.controller
- blocked_by: [product.saas.roadmap.phase3.analyst]
- estimate: 2w
- last_checked: 2026-01-23T21:44:23+01:00
<!-- content -->
- **Role**: Run the Recommender/Inventory logic (using Vertex AI Recommendations or custom RL).
- **Input**: State vector from the Local App.
- **Output**: Action (e.g., "Reorder 50 units") sent back to the Local App for user approval.

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
