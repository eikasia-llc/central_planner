import logging
import streamlit as st
import sys
import os
from pathlib import Path
import streamlit.components.v1 as components
import requests
import json

# Add current dir to path for imports
current_dir = Path(__file__).parent.resolve()
if str(current_dir) not in sys.path:
    sys.path.append(str(current_dir))

from log_config import setup_logging
setup_logging()

logger = logging.getLogger(__name__)

from git_manager import GitManager
import visualize_html

# Marker file: Flask writes this on successful edit, Streamlit reads/clears it.
# Bridges state between the two separate processes.
EDITS_PENDING_MARKER = Path(os.environ.get("REPO_MOUNT_POINT", str(current_dir.parent))) / ".edits_pending"

# Page Layout
st.set_page_config(layout="wide", page_title="Master Plan Visualization")

# --- State Initialization ---
if "git_error" not in st.session_state:
    st.session_state["git_error"] = False
if "has_unsaved_edits" not in st.session_state:
    st.session_state["has_unsaved_edits"] = False

# Pick up edits made via Flask (survives page refresh)
if EDITS_PENDING_MARKER.exists():
    st.session_state["has_unsaved_edits"] = True

# --- Git Startup Routine ---
repo_url = os.environ.get("GITHUB_REPO_URL", "https://github.com/eikasia-llc/central_planner.git")
# Use current project root as fallback if REPO_MOUNT_POINT is not set
repo_path = os.environ.get("REPO_MOUNT_POINT", str(current_dir.parent))
github_token = os.environ.get("GITHUB_TOKEN")

git = GitManager(repo_url, repo_path, github_token)

if "git_init_done" not in st.session_state:
    try:
        # Startup sync: clone or pull latest
        success, output = git.startup_sync(branch="main")
        st.session_state["git_init_done"] = True
        st.session_state["git_output"] = output
    except Exception as e:
        logger.exception("FATAL Git Initialization Error")
        st.session_state["git_error"] = True
        st.error(f"FATAL Git Initialization Error: {e}")
        st.stop()

# Title
st.title("Eikasia Master Plan")

# Sidebar
with st.sidebar:
    st.header("Actions")

    # Build title suffix from state flags
    suffix = ""
    if st.session_state["git_error"]:
        suffix += " ‼️"
    if st.session_state["has_unsaved_edits"]:
        suffix += " ❗"

    # Git Sync Section
    st.subheader(f"Repository Sync{suffix}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Git Pull ⬇️"):
            with st.spinner("Pulling..."):
                success, output = git.pull()
                st.session_state["git_output"] = output
                if success:
                    st.session_state["git_error"] = False
                    st.success("Pulled updates.")
                else:
                    st.session_state["git_error"] = True
                    logger.error("Git pull failed", extra={"output": output})
                    st.error("Pull failed.")
                st.rerun()

    with col2:
        if st.button("Git Push ⬆️"):
            with st.spinner("Pushing..."):
                success, output = git.push(message="Sync from Central Planner App")
                st.session_state["git_output"] = output
                if success:
                    st.session_state["has_unsaved_edits"] = False
                    # Clear the marker file
                    EDITS_PENDING_MARKER.unlink(missing_ok=True)
                    st.success("Pushed updates.")
                else:
                    st.session_state["git_error"] = True
                    st.session_state["has_unsaved_edits"] = True
                    logger.error("Git push failed", extra={"output": output})
                    st.error("Push failed.")
                st.rerun()

    # Console Output
    with st.expander("Console Output", expanded=False):
        st.code(st.session_state.get("git_output", "No output yet."), language="bash")

    st.divider()
    st.info("This view provides a interactive visualization of the underlying Master Plan markdown file.")

# Path Handling
# After Git Sync, MASTER_PLAN.md should be in content/planner relative to repo_path
target_file = Path(repo_path) / "content" / "planner" / "MASTER_PLAN.md"

if not target_file.exists():
    # Fallback to current structure if content/planner doesn't exist yet at mount point
    logger.error("MASTER_PLAN.md not found", extra={"path": str(target_file)})
    st.error(f"MASTER_PLAN.md not found at {target_file}")
    st.stop()

# File download — always available, independent of visualization
with st.sidebar:
    with open(target_file, "r", encoding="utf-8") as f:
        st.download_button(
            "📥 File Download",
            data=f.read(),
            file_name=target_file.name,
            mime="text/markdown",
        )

# Generate HTML
with st.spinner("Generating Visualization..."):
    try:
        # We need to tell visualize_html where D3 is. It should be in content/planner/
        d3_path = Path(repo_path) / "content" / "planner" / "d3.min.js"
        # Monkey patch D3_PATH in the module if needed, or pass it
        import visualize_html
        visualize_html.D3_PATH = str(d3_path)

        html_content = visualize_html.generate_html(
            str(target_file),
            embed_d3=True,
            edit_disabled=st.session_state["git_error"],
        )
    except Exception as e:
        logger.exception("Error generating HTML")
        st.error(f"Error generating HTML: {e}")
        st.stop()

# Render HTML
try:
    components.html(html_content, height=1000, scrolling=True)
except Exception as e:
    logger.exception("Error rendering component")
    st.error(f"Error rendering component: {e}")
