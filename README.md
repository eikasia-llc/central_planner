# Central Planner
- status: active

## Project Overview
This repository serves as a **meta-project** to organize and coordinate multiple different repositories and workflows using AI agents. It implements a **Markdown-YAML Hybrid Schema** to define detailed implementation plans that are readable by both humans and AI agents.

## Architecture

The system is built around a **Local-First, File-System-Centric Architecture**. Implementation plans are treated as computable graphs stored directly in the implementation code.

### Core Components
1.  **Markdown-YAML Schema**: A strict convention for defining hierarchical tasks with metadata using Markdown headers and YAML blocks.
2.  **Language Tools**: Python scripts to parse, valid, visualize, and manipulate these task trees.
3.  **AI Agents**: Specialized and generalist agent instructions to operate within this framework.

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

## Workflow & Tooling

### The Language System
The `language/` directory contains the "grammar" of our coordination system.

- **Visualization**: To see the current state of a plan or documentation:
  ```bash
  python3 language/visualization.py README.md
  ```

- **Operations**: To verify or manipulate plans:
  ```bash
  python3 language/test.py
  ```

### Agent Coordination
- **Generalists**: Refer to `AI_AGENTS/generalists/AGENTS.md` for the core workflow.
- **Specialists**: specialized agents (e.g., `REACT_ASSISTANT.md`) are located in `AI_AGENTS/specialists/`.

## Key Files
- **`MD_REPRESENTATION_CONVENTIONS.md`**: The definitive guide on how to write files in this repository.
- **`AGENTS.md`**: The entry point for any AI agent joining the project.
