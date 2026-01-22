# AGENTS.md

## SHORT ADVICE
- The whole trick is providing the AI Assistants with context, and this is done using the *.md files (AGENTS.md, AGENTS_LOG.md, and the AI_AGENTS folder)
- Learn how to work the Github, explained below.
- Keep logs of changes in AGENTS_LOG.md
- Make sure to execute the HOUSEKEEPING.md protocol often.
- Always ask several forms of verification, so because the self-loop of the chain of thought improves performance.
- Impose restrictions and constraints explicitly in the context.

## HUMAN-ASSISTANT WORKFLOW
1. Open the assistant and load the ai-agents-branch into their local repositories. Do this by commanding them to first of all read the AGENTS.md file.
2. Work on the ASSISTANT, making requests, modifying code, etc.
3. IMPORTANT: GIT MECHANISM
    3.1. This is basically solved in Antigravity, but Jules (and maybe Claude) push the changes into a newly generated branch. In my case, this is `jules-sync-main-v1-15491954756027628005`. **This is different from the `ai-agents-branch`!!**
    3.2. So what you need to do is merge the newly generated branch and the `ai-agents-branch` often. Usually in the direction from `jules-sync-main-v1-15491954756027628005` to `ai-agents-branch`. I do this by:
        3.2.1. Going to pull requests.
        3.2.2. New Pull request
        3.2.3. Base: `ai-agents-branch`, Compare: `jules-sync-main-v1-15491954756027628005` (arrow in the right direction).
        3.2.4. Follow through. It should allow to merge and there should not be incompatibilities. If there are incompatibilities, you can delete the `ai-agents-branch` and create a new one cloning the `jules-sync-main-v1-15491954756027628005` one. After deleting `ai-agents-branch`, go to the `jules-sync-main-v1-15491954756027628005` branch, look at the dropdown bar with the branches (not the link), and create a new copy.
4. It is very useful to use specialized agents for different sectors of the code. 
5. Enjoy!

## WORKFLOW & TOOLING

*   **Documentation Logs (`AGENTS_LOG.md`):**
    *   **Rule:** Every agent that performs a significant intervention or modifies the codebase **MUST** update the `AGENTS_LOG.md` file.
    *   **Action:** Append a new entry under the "Intervention History" section summarizing the task, the changes made, and the date.

## DEVELOPMENT RULES & CONSTRAINTS
1.  **Immutable Core Files:** Do not modify 
    *   If you need to change the logic of an agent or the model, you must create a **new version** (e.g., a subclass or a new file) rather than modifying the existing classes in place.
2.  **Consistency:** Ensure any modifications or new additions remain as consistent as possible with the logic and structure of the `main` branch.
3.  **Coding Conventions:** Always keep the coding conventions pristine.

## CONTEXT FINE-TUNING
You cannot "fine-tune" an AI agent (change its underlying neural network weights) with files in this repository. **However**, you **CAN** achieve a similar result using **Context**.

**How it works (The "Context" Approach):**
If you add textbooks or guides to the repository (preferably as Markdown `.md` or text files), agents can read them. You should then update the relevant agent instructions (e.g., `AI_AGENTS/LINEARIZE_AGENT.md`) to include a directive like:

> "Before implementing changes, read `docs/linearization_textbook.md` and `docs/jax_guide.md`. Use the specific techniques described in Chapter 4 for sparse matrix operations."

**Why this is effective:**
1.  **Specific Knowledge:** Adding a specific textbook helps if you want a *specific style* of implementation (e.g., using `jax.lax.scan` vs `vmap` in a particular way).
2.  **Domain Techniques:** If the textbook contains specific math shortcuts for your network types, providing the text allows the agent to apply those exact formulas instead of generic ones.

**Recommendation:**
If you want to teach an agent a new language (like JAX) or technique:
1.  Add the relevant chapters as **text/markdown** files.
2.  Update the agent's instruction file (e.g., `AI_AGENTS/LINEARIZE_AGENT.md`) to reference them.
3.  Ask the agent to "Refactor the code using the techniques in [File X]".

## LOCAL PROJECT DESCRIPTION

### Project Overview

### Setup & Testing
*   **Install Dependencies:**
*   **Run Backend:** 
*   **Run Frontend:** 
*   **Run Tests:** 

### Key Architecture & Logic

#### 1. Architecture (Monorepo)
*   **Backend (`backend/`)**: Python/FastAPI application handling all simulation logic, agent training, and state management.
*   **Frontend (`frontend/`)**: React/Vite application for the user interface, communicating with backend via REST API.

#### 2. Agents
*   **`backend/environment.py`**: The environment logic (p generation, reward calculation).
*   **`backend/agents.py`**: The Deep Q-Learning (DQN) agent implementation using PyTorch.

#### 3. Simulation Loop (`backend/simulation.py`)
*   **Step:**
    1.  Environment generates p.
    2.  Agents observe p and output actions (Recommend/Not Recommend).
    3.  Human (via React Interface) observes Agent actions and selects one.
    4.  Environment calculates outcome (Coin flip) and rewards.
    5.  Agents update their replay buffers and perform a training step.

### Key Files and Directories

#### Directory Structure
*   `backend/`: Contains the core Python logic (formerly `src/`).
    *   `api/`: FastAPI routes and session management.
    *   `engine/`: Pydantic models and simulation engine.
    *   `agents.py`: DQN Agent class.
    *   `environment.py`: BanditEnvironment class.
    *   `simulation.py`: GameSession class for legacy/notebook use.
*   `frontend/`: Contains the React application.
    *   `src/Controls.tsx`: Main game component.
    *   `src/App.tsx`: App entry with health check.
*   `tests/`: Contains unit tests.
*   `notebooks/`: Contains the legacy notebook interface.
    *   `experiment_interface.ipynb`: Interactive game (notebook version).

#### File Dependencies & Logic
`backend/simulation.py` depends on `backend/agents.py` and `backend/environment.py`.
The React frontend depends on the FastAPI backend running on port 8000.

**Legacy/Reference Implementation:**
No legacy, project starts from scratch.

**Vectorized Implementation (Fast):**
The DQN agents process the state `p` as a tensor. Training batches are processed in parallel using PyTorch.

**User Interface:**
The interface is provided via `ipywidgets` in `notebooks/experiment_interface.ipynb`, allowing the human subject to see recommendations and make choices.

**Testing & Verification:**
*   **`tests/test_mechanics.py`**: Verifies reward logic, buffer operations, and basic agent behavior.
