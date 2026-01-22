# Central Planner
- status: active

## Project Overview
This repository serves as a **meta-project** to organize and coordinate multiple different repositories and workflows using AI agents. It implements a **Markdown-YAML Hybrid Schema** to define detailed implementation plans that are readable by both humans and AI agents.

## The Markdown-YAML Protocol

The project uses a strict **Markdown-YAML Hybrid Schema** to treat documentation as a computable graph.

### Structure & Hierarchy
- **Hierarchy**: Defined by standard Markdown headers (`#`, `##`, `###`). The nesting level indicates parent-child relationships, allowing for infinite depth.
- **Dependencies**:
    - **Implicit**: A child node is strictly dependent on its parent.
    - **Explicit**: Defined in metadata (e.g., `blocked_by: [node_id]`).
- **Metadata**: Every node (header) must be immediately followed by a YAML block defining its attributes.

**Example Node:**
```markdown
## Implement Login Feature
- status: in-progress
- owner: @frontend-agent
- priority: high
```

### The Language System (Tooling)
A suite of Python scripts in the `language/` directory allows agents and humans to interact with this protocol programmatically:

- **Parsing**: `md_parser.py` converts raw Markdown into structured Python objects, validating schema compliance.
- **Visualization**: `visualization.py` renders the task tree in the terminal, showing structure and status at a glance.
- **Standardization**: `migrate.py` automatically converts standard Markdown files into the Protocol format by injecting default metadata.
- **Import**: `importer.py` converts legacy documents (`.docx`, `.pdf`) into Protocol-compliant Markdown.
- **Operations**: `operations.py` allows for complex tree manipulations, such as merging subtrees or extending plans.

## Directory Structure

```
central_planner/
├── AGENTS.md                     # General Agent Guidelines & Workflow
├── README.md                     # Project Documentation (This File)
├── AI_AGENTS/                    # Agent Instructions
│   ├── specialists/              # Specialized Agent Protocols (e.g., React, RecSys)
│   └── generalists/              # General Project Protocols (Setup, Housekeeping)
├── language/                     # Tooling for the Communication System
│   ├── md_parser.py              # Parses & Validates MD/YAML files
│   ├── visualization.py          # Visualizes task trees
│   ├── operations.py             # Merges and Extends task trees
│   ├── migrate.py                # Heuristic migration tool
│   └── test.py                   # Test suite for the language tools
└── MD_REPRESENTATION_CONVENTIONS.md # Specification of the Schema
```



## Key Files
- **`MD_REPRESENTATION_CONVENTIONS.md`**: The definitive guide on how to write files in this repository.
- **`AGENTS.md`**: The entry point for any AI agent joining the project.
