# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Central Planner is a meta-project coordination system that uses a **Markdown-JSON Hybrid Schema** to define implementation plans readable by both humans and AI agents. The system treats documentation as a computable graph that can be losslessly converted between Markdown and JSON formats.

**Production App**: https://central-planner-app-216559257034.us-central1.run.app

## Essential Reading

Before working in this repository, read these files in order:
1. **MD_CONVENTIONS.md** - The strict schema rules for all Markdown files
2. **AGENTS.md** - General workflow and context management
3. **README.md** - Project structure and overview

## Common Commands

### Local Development

Run the Streamlit app locally:
```bash
pip install -r requirements.txt
streamlit run src/app.py
```

### Markdown Parsing & Validation

Parse and validate a Markdown file (outputs JSON):
```bash
python src/planner_lib/md_parser.py <input.md>
python src/planner_lib/md_parser.py <input.md> <output.json>
```

### Visualization

Generate interactive HTML visualization of MASTER_PLAN.md:
```bash
python src/visualize_html.py
```

### Cloud Deployment

Build and deploy to Google Cloud Run:
```bash
# Build using Cloud Build (recommended)
gcloud builds submit --config cloudbuild.yaml .

# Deploy to Cloud Run
gcloud run deploy central-planner-app \
    --image us-central1-docker.pkg.dev/eikasia-ops/central-planner-repo/central-planner-app:latest \
    --region us-central1 \
    --platform managed \
    --set-env-vars="REPO_MOUNT_POINT=/tmp/central_planner_repo,GITHUB_REPO_URL=https://github.com/eikasia-llc/central_planner.git" \
    --set-secrets="GITHUB_TOKEN=GITHUB_TOKEN:latest"
```

See INFRASTRUCTURE.md for detailed deployment instructions.

## Critical Architecture Concepts

### The Markdown-JSON Hybrid Schema

This is the **core concept** of the entire system. Every Markdown file must follow strict conventions:

1. **Headers define hierarchy**: `#`, `##`, `###` create parent-child relationships
2. **Metadata blocks**: Immediately after each header, use bullet list format:
   ```markdown
   ## Task Name
   - status: in-progress
   - type: task
   - owner: dev-1
   - id: project.component.task
   - blocked_by: [other-task-id]
   <!-- content -->
   Task description goes here...
   ```
3. **Separator is mandatory**: `<!-- content -->` separates metadata from content
4. **Dependencies**:
   - Implicit: child nodes depend on parents
   - Explicit: use `blocked_by` to create DAG relationships
5. **Global IDs**: Always use `id` field for robust cross-file references

**Why this matters**: The parser (`src/planner_lib/md_parser.py`) expects this exact format. Breaking these rules causes parsing failures.

### Node Structure (Python)

The `Node` class in `md_parser.py` represents the parsed tree:
- `level`: Header depth (1-6)
- `title`: Header text
- `metadata`: Dict of key-value pairs
- `content`: Free-form Markdown after separator
- `children`: List of child Nodes

Convert between formats:
- `node.to_dict()` → JSON-serializable dict
- `Node.from_dict(data)` → Reconstruct Node tree
- `node.to_markdown()` → Generate Markdown text

### Visualization Pipeline

1. `md_parser.py` parses Markdown → Node tree
2. `visualize_html.py` converts Node tree → JSON with dependencies
3. D3.js renders interactive tree + dependency DAG
4. Streamlit app (`src/app.py`) embeds the visualization

Dependencies are extracted by finding `blocked_by` fields and matching them to node `id` fields.

### Git Integration

The Streamlit app uses `GitManager` (in `src/git_manager.py`) to:
- Clone the repository on startup to ephemeral `/tmp` storage
- Pull/push changes via UI buttons
- Sync the `content/planner/MASTER_PLAN.md` file

**Important**: Cloud Run instances are ephemeral. All persistence is via GitHub.

## File Organization

```
src/
├── app.py                      # Streamlit dashboard entry point
├── git_manager.py              # Git operations (clone, pull, push)
├── visualize_html.py           # D3 visualization generator
└── planner_lib/
    ├── md_parser.py            # Core Markdown parser (Node class)
    ├── cli_utils.py            # CLI argument handling utilities
    └── migrate.py              # Schema migration tool

content/planner/                # Planning content (Git-persisted)
├── MASTER_PLAN.md              # Central plan file
└── subplans/                   # Modular sub-plans

manager/planner/                # Repository coordination tools
├── update_master_plan.py       # Merge external plans
├── visualize_graph.py          # Graph visualization
└── visualize_plan.py           # Plan visualization
```

## Metadata Field Reference

Standard fields (see MD_CONVENTIONS.md for full spec):
- `status`: `todo`, `in-progress`, `done`, `blocked`, `active`
- `type`: `plan`, `task`, `recurring`, `agent_skill`, `protocol`, `guideline`, `log`, `context`
- `owner`: Agent or user assigned (e.g., `dev-1`, `claude`)
- `estimate`: Time estimate (e.g., `1d`, `4h`)
- `blocked_by`: List of dependency IDs (e.g., `[task-a, task-b]`)
- `priority`: `draft`, `low`, `medium`, `high`, `critical`
- `id`: Unique identifier (e.g., `project.component.task`)
- `context_dependencies`: Map of semantic aliases to file paths
- `last_checked`: ISO-8601 timestamp of last modification

## Working with the Schema

### When Adding New Nodes

1. **Always generate an `id`**: Use dot-notation (e.g., `feature.auth.login`)
2. **Add `<!-- content -->` separator**: Required between metadata and content
3. **Update `last_checked`**: Use current ISO-8601 date when modifying
4. **Validate**: Run `python src/planner_lib/md_parser.py <file.md>` to check

### When Creating Dependencies

Use `blocked_by` with node IDs:
```markdown
## Backend API
- id: backend.api
- status: done
<!-- content -->

## Frontend Integration
- id: frontend.integration
- status: in-progress
- blocked_by: [backend.api]
<!-- content -->
Depends on backend.api being complete.
```

### Agent Logging

All significant interventions must be logged in `AGENTS_LOG.md`:
- Date of change
- Summary of task
- Files modified
- Agent or user who made the change

## Context Management

This repository uses a **context-first** approach for AI agents:

1. **Context Dependencies**: Files can declare required reading via `context_dependencies` metadata
2. **Recursive Resolution**: Agents should read dependencies depth-first (if A depends on B, and B depends on C, read C → B → A)
3. **No Fine-tuning**: Instead of model fine-tuning, provide domain knowledge as Markdown files and instruct agents to read them

Example:
```markdown
## Linear Algebra Module
- context_dependencies: {"textbook": "docs/linalg.md", "conventions": "MD_CONVENTIONS.md"}
<!-- content -->
Before implementing, read the textbook and conventions.
```

## Cloud Deployment Notes

- **Container**: Docker image built from `Dockerfile`, deployed to Google Cloud Run
- **Build**: Use `cloudbuild.yaml` for faster builds (internal GCP networking)
- **Secrets**: GitHub token stored in Secret Manager, injected at runtime
- **Storage**: Ephemeral `/tmp` storage; GitHub is source of truth
- **Auth**: Identity-Aware Proxy (IAP) for user authentication

## Common Pitfalls

1. **Missing separator**: Forgetting `<!-- content -->` causes metadata to bleed into content
2. **Invalid status values**: Parser validates against enum; check MD_CONVENTIONS.md for allowed values
3. **Circular dependencies**: The system expects a DAG; circular `blocked_by` will break visualization
4. **No node ID**: Without `id`, cross-file references break
5. **Inconsistent spacing**: The parser expects exact bullet format: `- key: value`

## Integration Points

- **Streamlit**: `app.py` is the main entry point
- **D3.js**: Embedded in `visualize_html.py` template for tree visualization
- **GitHub**: All persistence via git operations in `git_manager.py`
- **GCP Secret Manager**: Credentials for GitHub access
- **Cloud Run**: Serverless container hosting with auto-scaling
