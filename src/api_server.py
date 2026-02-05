"""
Flask API Server for Markdown File Editing

Provides REST API endpoints for applying edits to markdown files
with line number tracking.
"""

import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from planner_lib.file_editor import apply_edits_to_file, EditValidationError

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
        # Get JSON payload
        edits = request.json

        if not edits:
            return jsonify({
                "success": False,
                "error": "No JSON payload provided"
            }), 400

        # Apply edits
        success, message = apply_edits_to_file(edits)

        if success:
            return jsonify({
                "success": True,
                "message": message
            })
        else:
            return jsonify({
                "success": False,
                "error": message
            }), 400

    except EditValidationError as e:
        return jsonify({
            "success": False,
            "error": f"Validation error: {str(e)}"
        }), 400

    except Exception as e:
        # Log the full error for debugging
        app.logger.error(f"Error in save_edits: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
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
