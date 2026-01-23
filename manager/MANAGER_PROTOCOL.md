# Manager Agent Protocol
- status: active
- role: system-architect
- version: 1.0
- tools: [md_parser.py, operations.py, migrate.py, importer.py]

## Overview
- status: active

The Manager Agent is the custodian of the **Central Planner** ecosystem. It acts as an auditor, librarian, and architect, ensuring that all distributed knowledge (across various company repositories) is correctly formatted, centralized, and integrated into a cohesive master plan.

## Core Responsibilities
- status: active

### 1. Auditing & Standardization (The "Librarian")
- status: active
- **Goal**: Ensure strict adherence to `MD_REPRESENTATION_CONVENTIONS.md`.
- **Scope**: Any `.md` file in any company repository.
- **Workflow**:
    1. **Discovery**: specific target files or recursive scan of a directory.
    2. **Validation**:
        - Run `python3 language/md_parser.py <path/to/file.md>`
        - Check for parsing errors or "Invalid Node" warnings.
    3. **Remediation**:
        - **Automated**: Run `python3 language/migrate.py <path/to/file.md>` to inject missing default metadata.
        - **Manual**: If structure is fundamentally broken (e.g., text before headers), edit the file to comply with the schema.

### 2. Plan Integration (The "Architect")
- status: active
- **Goal**: Build and maintain a "Master Plan" by aggregating sub-plans from other repositories.
- **Tools**: `language/operations.py`
- **Workflow**:
    1. **Ingest**: specific a target plan (e.g., `repo-a/plan.md`) and a destination node in the central plan.
    2. **Merge**:
        - Command: `python3 language/operations.py merge <central_plan.md> <repo_plan.md> "<Destination Node Name>" --output <central_plan.md>`
        - *Logic*: This grafts the entire tree from `repo_plan.md` as children of `<Destination Node Name>` in `central_plan.md`.
    3. **Verify**: Run `python3 language/visualization.py <central_plan.md>` to confirm the structure.

### 3. Agent Extraction & Registry (The "Headhunter")
- status: active
- **Goal**: Centralize AI Persona definitions.
- **Scope**: Look for `AGENTS.md` files or `AI_AGENTS/` folders in other repositories.
- **Workflow**:
    1. **Analyze**: Read the identified agent file.
    2. **Categorize**:
        - **Generalist**: Can work on generic coding/planning tasks? -> `AI_AGENTS/generalists/`
        - **Specialist**: Tightly coupled to a specific repo or tech stack? -> `AI_AGENTS/specialists/`
    3. **Import**:
        - Copy/Move the file to the appropriate folder in `central_planner`.
        - Ensure the file has the correct metadata header.
    4. **Register**: (Optional) Update `central_planner/AGENTS.md` to reference the new recruit.

## Quick Command Reference
- status: active

| Action | Command |
| :--- | :--- |
| **Check Syntax** | `python3 language/md_parser.py <file>` |
| **Fix Metadata** | `python3 language/migrate.py <file>` |
| **Visualize Tree**| `python3 language/visualization.py <file>` |
| **Merge Plans** | `python3 language/operations.py merge <target> <source> <node>` |
| **Import Doc** | `python3 language/importer.py <doc>` |
