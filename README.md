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
A suite of Python scripts in `manager/planner/lib/` (previously `language/`) allows the planner to interact with this protocol programmatically:

- **Parsing**: `md_parser.py` converts raw Markdown into structured Python objects, validating schema compliance.
- **Visualization**: `visualize_graph.py` generates a visualization of the Master Plan.
- **Migration**: `migrate.py` standardizes Markdown files.

## Repository Manager
- status: active
<!-- content -->
The `manager/` directory contains tools for coordinating multiple external repositories:

- **Integration**: `update_master_plan.py` integrates these external plans into the central `MASTER_PLAN.md`.

## Directory Structure
- status: active
<!-- content -->
```
central_planner/
├── AGENTS.md                     # General Agent Guidelines & Workflow
├── AGENTS_LOG.md                 # Project-wide agent activity log
├── README.md                     # Project Documentation (This File)
├── MD_CONVENTIONS.md             # Specification of the Schema
├── manager/                      # Repository Management & Planning
│   └── planner/                  # Central Planning and Master Plan management
└── bin/                          # Binary/Executable wrappers for tools
```

## Key Files
- status: active
<!-- content -->
- **`MD_CONVENTIONS.md`**: The definitive guide on how to write files in this repository.
- **`AGENTS.md`**: The entry point for any AI agent joining the project.
