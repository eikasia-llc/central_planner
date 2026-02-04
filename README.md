# Central Planner
- status: active
- type: guideline
- context_dependencies: {"conventions": "MD_CONVENTIONS.md", "agents": "AGENTS.md"}
<!-- content -->

## Project Overview
- status: active
<!-- content -->
This repository serves as a **meta-project** to organize and coordinate multiple different repositories and workflows using AI agents. It implements a **Markdown-JSON Hybrid Schema** to define detailed implementation plans that are readable by both humans and AI agents, and losslessly convertible to JSON for programmatic manipulation.

## The Markdown-JSON Protocol
- status: active
<!-- content -->
The project uses a strict **Markdown-JSON Hybrid Schema** to treat documentation as a computable graph. Every Markdown file following this schema can be losslessly converted to JSON and back.

### Structure & Hierarchy
- status: active
<!-- content -->
- **Hierarchy**: Defined by standard Markdown headers (`#`, `##`, `###`). The nesting level indicates parent-child relationships, allowing for infinite depth.
- **Dependencies**:
    - **Implicit**: A child node is strictly dependent on its parent.
    - **Explicit (DAG)**: Defined in metadata using `blocked_by` (e.g., `blocked_by: [task-a, task-b]`). This allows defining complex Directed Acyclic Graphs where a node depends on multiple independent predecessors.
- **Identification**: 
    - **Title**: Default identification method.
    - **Global ID**: An optional `id` metadata field (e.g., `id: component.backend`). This is the **preferred** method for robust cross-file operations (merging/linking), as it persists even if the human-readable title changes.
- **Separator**: A `<!-- content -->` line separates metadata from content, ensuring unambiguous parsing.
- **Metadata**: Every node (header) must be immediately followed by a METADATA block defining its attributes.

**Example Node:**
```markdown

## Implement Login Feature
- id: feature.auth.login
- status: in-progress
- owner: @frontend-agent
- priority: high
- blocked_by: [feature.auth.backend, infra.db.setup]
<!-- content -->
Description of the login feature implementation...
```

### The Language System (Tooling)
- status: active
<!-- content -->
A suite of Python scripts in `src/planner_lib/` (previously `language/`) allows the planner to interact with this protocol programmatically:

- **Parsing**: `md_parser.py` (in `src/planner_lib`) converts raw Markdown into structured Python objects, validating schema compliance.
- **Visualization**: `visualize_html.py` (in `src/`) generates an interactive D3 visualization of the Master Plan.

## Repository Manager
- status: active
<!-- content -->
The `manager/` directory contains tools for coordinating multiple external repositories:

- **Integration**: `update_master_plan.py` (in `manager/planner/`) integrates these external plans into the central `MASTER_PLAN.md`.

## Directory Structure
- status: active
<!-- content -->
```
central_planner/
├── AGENTS.md                     # General Agent Guidelines & Workflow
├── AGENTS_LOG.md                 # Project-wide agent activity log
├── README.md                     # Project Documentation (This File)
├── INFRASTRUCTURE.md             # Cloud Infrastructure & Deployment guide
├── MD_CONVENTIONS.md             # Specification of the Schema
├── Dockerfile                    # Containerization for Cloud Run
├── src/                          # Application source code
│   ├── app.py                    # Streamlit Dashboard (Entry Point)
│   ├── git_manager.py            # Git Sync logic
│   ├── visualize_html.py         # D3 Visualization generator
│   └── planner_lib/              # Core logic & Markdown Parser
├── content/                      # Planning content (Git Persisted)
│   └── planner/                  # Central Planning files (MASTER_PLAN.md, etc.)
├── manager/                      # Repository Management Tooling
└── bin/                          # Binary/Executable wrappers for tools
```

## Running & Deployment

### Local Development
To run the Streamlit dashboard locally:
```bash
pip install -r requirements.txt
streamlit run src/app.py
```

### Cloud Run Deployment
Refer to [INFRASTRUCTURE.md](file:///home/zeta/src/eikasia/control_tower/repositories/central_planner/INFRASTRUCTURE.md) for detailed instructions.

Quick Deploy:
```bash
# Build
gcloud builds submit --tag us-central1-docker.pkg.dev/eikasia-ops/central-planner-repo/central-planner:latest .

# Deploy
gcloud run deploy central-planner --image us-central1-docker.pkg.dev/eikasia-ops/central-planner-repo/central-planner:latest --region us-central1
```

## Key Files
- status: active
<!-- content -->
- **`MD_CONVENTIONS.md`**: The definitive guide on how to write files in this repository.
- **`AGENTS.md`**: The entry point for any AI agent joining the project.
