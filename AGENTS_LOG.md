# Agents Log

Most recent event comes first

## Intervention History

### Feature: Remove Metadata Tool
**Date:** 2026-01-22
**AI Assistant:** Antigravity
**Summary:** Created `remove_meta.py` to reverse `migrate.py` effects and clean incomplete content.
- **Goal:** Allow removing metadata from markdowns and strip incomplete sections/content.
- **Implementation:**
    - Created `language/remove_meta.py` with strict metadata detection logic.
    - Added flags `--remove-incomplete-content` and `--remove-incomplete-sections`.
    - Created symlink `bin/language/remove_meta` -> `../../util/sh2py3.sh`.
- **Files Modified:** `language/remove_meta.py` [NEW], `bin/language/remove_meta` [NEW].

### Feature: CLI Improvements
**Date:** 2026-01-22
**AI Assistant:** Antigravity
**Summary:** Improved Python CLIs in `manager` and `language` to be POSIX-friendly and support flexible I/O modes.
- **Goal:** Standardize CLI usage and support single/multi-file processing with checks.
- **Implementation:**
    - Created `language/cli_utils.py` for shared arg parsing.
    - Updated `migrate.py`, `importer.py` to support `-I` (in-line) and repeated `-i/-o`.
    - Updated `md_parser.py`, `visualization.py` to support file output.
    - Added `-h` to all tools.
- **Files Modified:** `language/*.py`, `manager/*.py`.

### Feature: Shell Wrapper for Python Scripts
**Date:** 2026-01-22
**AI Assistant:** Antigravity
**Summary:** Created a generic shell wrapper `sh2py3.sh` and symlinks for python scripts.
- **Goal:** Allow execution of python scripts in `manager/` and `language/` from a central `bin/` directory.
- **Implementation:**
    - Created `util/sh2py3.sh` to determine script path from symlink invocation and execute with python/python3.
    - Created `bin/manager` and `bin/language` directories.
    - Created symlinks in `bin/` mapping to `util/sh2py3.sh` for all `.py` files in `manager/` and `language/`.
- **Files Modified:** `util/sh2py3.sh` [NEW], `bin/` directories [NEW].



### Housekeeping Report (Initial)

_TBD_


## Example History

Not real. Use as reference when updating this file.

### Bug Fix: Advanced Analysis (Shape Mismatch)
**Date:** 2024-05-22
**AI Assistant:** Antigravity, Claude Opus 4.5 (Thinking)
**Summary:** Fixed RuntimeError in `advanced_experiment_interface.ipynb`.
- **Issue:** `compute_policy_metrics` in `src/analysis.py` passed 1D inputs `(100, 1)` to agents expecting 2D inputs `(100, 2)`.
- **Fix:** Created `src/advanced_analysis.py` with `compute_advanced_policy_metrics`.
- **Details:** The new function constructs inputs as `[p, t]` with `t` fixed at 0 (default).
- **Files Modified:** `src/advanced_simulation.py` updated to use the new analysis function.

### Housekeeping Report (Initial)
**Date:** 2024-05-21
**Summary:** Executed initial housekeeping protocol.
**AI Assitant:**
- **Dependency Network:**
- **Tests:**
