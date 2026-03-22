"""
Flask API Server for Markdown File Editing

Provides REST API endpoints for applying edits to markdown files
with line number tracking.
"""

import logging
import os
import sys
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from log_config import setup_logging
setup_logging()

from pathlib import Path
from planner_lib.file_editor import apply_edits_to_file, EditValidationError

logger = logging.getLogger(__name__)

# Marker file: signals to Streamlit that edits have been made since last push.
EDITS_PENDING_MARKER = Path(os.environ.get(
    "REPO_MOUNT_POINT", os.path.join(current_dir, os.pardir)
)) / ".edits_pending"

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/api/save_edits', methods=['POST'])
def save_edits():
    """
    Apply edits to a markdown file.

    Expected JSON payload:
    {
        "file_path": "/path/to/file.md",
        "node_identifier": {
            "id": "node.id",
            "title": "Node Title"
        },
        "metadata_edits": {
            "key": {"value": "new_value", "line_number": 123}
        },
        "content_edit": {
            "value": "new content",
            "start_line": 125,
            "end_line": 127
        }
    }

    Returns:
        JSON response with success status and message
    """
    try:
        # Get JSON payload — log raw body on parse errors
        raw_body = request.get_data(as_text=True)
        try:
            edits = request.json
        except Exception:
            logger.exception("save_edits JSON parse error", extra={"raw_body": raw_body[:1_048_576]})
            return jsonify({
                "success": False,
                "error": "Invalid JSON payload"
            }), 400

        if not edits:
            logger.warning("save_edits empty payload", extra={"raw_body": (raw_body or "")[:1_048_576]})
            return jsonify({
                "success": False,
                "error": "No JSON payload provided"
            }), 400

        node_id = edits.get("node_identifier", {}).get("id", "unknown")
        file_path = edits.get("file_path", "unknown")
        logger.info("save_edits called", extra={"node_id": node_id, "file_path": file_path})

        # Apply edits
        success, message = apply_edits_to_file(edits)

        if success:
            logger.info("save_edits succeeded", extra={"node_id": node_id, "file_path": file_path})
            EDITS_PENDING_MARKER.touch()
            return jsonify({
                "success": True,
                "message": message
            })
        else:
            logger.warning("save_edits failed", extra={"node_id": node_id, "file_path": file_path, "error": message})
            return jsonify({
                "success": False,
                "error": message
            }), 400

    except EditValidationError as e:
        logger.warning("save_edits validation error", extra={"error": str(e)})
        return jsonify({
            "success": False,
            "error": f"Validation error: {str(e)}"
        }), 400

    except Exception as e:
        logger.exception("save_edits unexpected error")
        tb_lines = traceback.format_exception(type(e), e, e.__traceback__)
        tb_short = "".join(tb_lines[-4:])
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}",
            "trace": tb_short
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "markdown-editor-api"
    })


@app.route('/', methods=['GET'])
def index():
    """Root endpoint with API information."""
    return jsonify({
        "service": "Markdown File Editor API",
        "version": "1.0",
        "endpoints": {
            "/api/save_edits": "POST - Apply edits to markdown files",
            "/api/health": "GET - Health check"
        }
    })


if __name__ == '__main__':
    # Get port from environment or default to 8502
    port = int(os.environ.get('API_PORT', 8502))
    host = os.environ.get('API_HOST', '0.0.0.0')

    print(f"Starting Markdown Editor API server on {host}:{port}")
    app.run(host=host, port=port, debug=False)
