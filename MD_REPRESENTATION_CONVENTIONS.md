# Markdown-YAML Hybrid Schema Conventions

This document defines the strict conventions for the Markdown-YAML Hybrid Schema used in this project for hierarchical task coordination and agentic planning.

## Core Principle

The system uses a **Markdown headers** to define the structural hierarchy (the nodes) and **YAML Frontmatter-style blocks** (immediately following the header) to define structured metadata.

## Schema Rules

### 1. Hierarchy & Nodes
- **Headers**: Use standard Markdown headers (`#`, `##`, `###`) to define the hierarchy.
- **Nesting**: 
    - `#` is the Root/Document Title (usually only one per file).
    - `##` are Top-Level Tasks/Features.
    - `###` are Subtasks.
    - And so on.
- **Implicit Dependency**: A header is implicitly dependent on its parent header.

### 2. Metadata Blocks
- **Location**: Metadata MUST be placed **immediately** after the header, before any free-form text.
- **Format**: A YAML block. It works best as a bulleted list of key-value pairs, which most parsers can interpret as YAML (or we can use strict YAML blocks if preferred, but the spec suggests "YAML Key-Value Pairs (immediately following header)"). 
- **Preferred Format**: A strict list of key-value pairs.

**Example:**

```markdown
## Implement User Auth
- status: in-progress
- owner: dev-1
- estimate: 3d
- blocked_by: []
```

### 3. Allowed Fields

The following fields are standard, but the schema allows extensibility.

| Field | Type | Description |
| :--- | :--- | :--- |
| `status` | `enum` | `todo`, `in-progress`, `done`, `blocked` |
| `owner` | `string` | The agent or user assigned to this (e.g., `dev-1`, `claude`) |
| `estimate` | `string` | Time estimate (e.g., `1d`, `4h`) |
| `blocked_by`| `list` | List of explicit dependencies (IDs or relative paths) |
| `priority` | `enum` | `low`, `medium`, `high`, `critical` (Optional) |

### 4. Context & Description
- Any text following the metadata block is considered "Context" or "Description".
- It can contain free-form Markdown, code blocks, images, etc.

## Examples

### Valid Node
```markdown
### Database Schema
- status: done
- owner: dev-2
- estimate: 1d

Set up PostgreSQL schema for users and sessions.
```

### Invalid Node (Metadata not immediate)
```markdown
### Database Schema

Some text here first.

- status: done
```
*Error: Metadata block must immediately follow the header.*

### Invalid Node (Bad indentation/YAML)
```markdown
### Database Schema
status: done
owner: dev-2
```
*Warning: While some parsers might handle this, prefer bullet points `- key: value` for readability and stricter parsing.*

## Parsing Logic (for Developers)

1. **Scan for Headers**.
2. **Look ahead** at the lines immediately following the header.
3. **Parse lines** that match the YAML key-value pattern (`- key: value` or `key: value`) until a blank line or non-matching line is found.
6. **Everything else** until the next header of equal or higher level is "Content".

## Tooling Reference

The following Python scripts are available in `scripts/` to interact with this schema:

### 1. `scripts/md_parser.py`
- **Purpose**: Parses `.md` files into a Python object tree and validates schema compliance.
- **Usage**: `python3 scripts/md_parser.py <file.md>`
- **Output**: JSON representation of the tree or validation errors.

### 2. `scripts/visualization.py`
- **Purpose**: Visualizes the task tree in the terminal with metadata.
- **Usage**: `python3 scripts/visualization.py <file.md>`
- **Output**: Unicode tree visualization.

### 3. `scripts/operations.py`
- **Purpose**: Manipulate task trees (merge, extend).
- **Usage**:
    - **Merge**: `python3 scripts/operations.py merge <target.md> <source.md> "<Target Node Title>" [--output <out.md>]`
        - Inserts the source tree as children of the specified target node.
    - **Extend**: `python3 scripts/operations.py extend <target.md> <source.md> [--output <out.md>]`
        - Appends the source tree's top-level items to the target tree's top level.

### 4. `scripts/migrate.py`
- **Purpose**: Heuristically adds default metadata to standard Markdown headers to make them schema-compliant.
- **Usage**: `python3 scripts/migrate.py <file.md> [file2.md ...]`
- **Effect**: Modifies files in-place by injecting `- status: active` after headers that lack metadata.

## Migration Guidelines

When migrating existing documentation to this schema:
1. **Run the Migration Script**: Use `scripts/migrate.py` to add baseline metadata.
2. **Review and Refine**: Manually update the `status` fields (e.g., change `active` to `draft` or `deprecated` where appropriate) and add `owner` information.
3. **Structure Check**: Ensure the hierarchy makes sense as a task/node tree.

