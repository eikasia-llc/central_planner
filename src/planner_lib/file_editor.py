"""
File Editor Module - Applies edits to markdown files using line number tracking.

This module provides functionality to:
1. Apply metadata edits (replace specific metadata lines)
2. Apply content edits (replace content blocks)
3. Validate edits before application
4. Handle errors gracefully
"""

import os
import json
from typing import Dict, Any, List, Tuple


class EditValidationError(Exception):
    """Raised when edit validation fails."""
    pass


class FileEditor:
    """Handles applying edits to markdown files with line number tracking."""

    def apply_edits(self, edits: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Apply edits to a markdown file.

        Args:
            edits: Dictionary containing:
                - file_path: Path to the file to edit
                - node_identifier: {id: <id>, title: <title>} for identifying the node
                - metadata_edits: {key: {value: <val>, line_number: <num>}}
                - content_edit: {value: <text>, start_line: <num>, end_line: <num>}

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # 1. Validate edits
            self._validate_edits(edits)

            file_path = edits['file_path']

            # 2. Read file as lines
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # 3. Collect all edits with line numbers
            all_edits = self._collect_all_edits(edits, len(lines))

            # 4. Sort by line number DESCENDING (bottom to top)
            all_edits.sort(key=lambda x: x[0], reverse=True)

            # 5. Apply edits
            for line_num, edit_type, edit_data in all_edits:
                if edit_type == 'metadata':
                    key, value = edit_data
                    lines = self._apply_metadata_edit(lines, line_num, key, value)
                elif edit_type == 'content':
                    start, end, value = edit_data
                    lines = self._apply_content_edit(lines, start, end, value)

            # 6. Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)

            return True, f"Successfully applied edits to {os.path.basename(file_path)}"

        except EditValidationError as e:
            return False, f"Validation error: {str(e)}"
        except FileNotFoundError:
            return False, f"File not found: {edits.get('file_path', 'unknown')}"
        except PermissionError:
            return False, f"Permission denied: {edits.get('file_path', 'unknown')}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"

    def _validate_edits(self, edits: Dict[str, Any]) -> None:
        """
        Validate edit structure and content.

        Raises:
            EditValidationError: If validation fails
        """
        # Check required fields
        if 'file_path' not in edits:
            raise EditValidationError("Missing required field: file_path")

        if 'node_identifier' not in edits:
            raise EditValidationError("Missing required field: node_identifier")

        # Check file exists
        file_path = edits['file_path']
        if not os.path.exists(file_path):
            raise EditValidationError(f"File does not exist: {file_path}")

        # Validate metadata edits if present
        if 'metadata_edits' in edits:
            metadata_edits = edits['metadata_edits']
            if not isinstance(metadata_edits, dict):
                raise EditValidationError("metadata_edits must be a dictionary")

            for key, edit_info in metadata_edits.items():
                if not isinstance(edit_info, dict):
                    raise EditValidationError(f"Invalid metadata edit format for key '{key}'")
                if 'value' not in edit_info:
                    raise EditValidationError(f"Missing 'value' in metadata edit for key '{key}'")
                if 'line_number' not in edit_info:
                    raise EditValidationError(f"Missing 'line_number' in metadata edit for key '{key}'")
                if not isinstance(edit_info['line_number'], int) or edit_info['line_number'] < 0:
                    raise EditValidationError(f"Invalid line_number for key '{key}': must be non-negative integer")

        # Validate content edit if present
        if 'content_edit' in edits:
            content_edit = edits['content_edit']
            if not isinstance(content_edit, dict):
                raise EditValidationError("content_edit must be a dictionary")
            if 'value' not in content_edit:
                raise EditValidationError("Missing 'value' in content_edit")
            if 'start_line' not in content_edit:
                raise EditValidationError("Missing 'start_line' in content_edit")
            if 'end_line' not in content_edit:
                raise EditValidationError("Missing 'end_line' in content_edit")

            start = content_edit['start_line']
            end = content_edit['end_line']

            if not isinstance(start, int) or start < 0:
                raise EditValidationError("start_line must be non-negative integer")
            if not isinstance(end, int) or end < 0:
                raise EditValidationError("end_line must be non-negative integer")
            if start > end:
                raise EditValidationError(f"start_line ({start}) must be <= end_line ({end})")

        # Must have at least one type of edit
        if 'metadata_edits' not in edits and 'content_edit' not in edits:
            raise EditValidationError("No edits provided (need metadata_edits or content_edit)")

    def _collect_all_edits(self, edits: Dict[str, Any], file_length: int) -> List[Tuple[int, str, Any]]:
        """
        Collect all edits into a list with (line_number, edit_type, edit_data).

        Args:
            edits: Edit dictionary
            file_length: Number of lines in the file (for bounds checking)

        Returns:
            List of (line_number, edit_type, edit_data) tuples
        """
        all_edits = []

        # Collect metadata edits
        if 'metadata_edits' in edits:
            for key, edit_info in edits['metadata_edits'].items():
                line_num = edit_info['line_number']
                value = edit_info['value']

                # Validate line number within bounds
                if line_num >= file_length:
                    raise EditValidationError(
                        f"Line number {line_num} for key '{key}' exceeds file length ({file_length})"
                    )

                all_edits.append((line_num, 'metadata', (key, value)))

        # Collect content edit
        if 'content_edit' in edits:
            content_edit = edits['content_edit']
            start = content_edit['start_line']
            end = content_edit['end_line']
            value = content_edit['value']

            # Validate line numbers within bounds
            if end > file_length:
                raise EditValidationError(
                    f"Content end_line {end} exceeds file length ({file_length})"
                )

            all_edits.append((start, 'content', (start, end, value)))

        return all_edits

    def _apply_metadata_edit(self, lines: List[str], line_num: int, key: str, value: Any) -> List[str]:
        """
        Apply a metadata edit to a specific line.

        Args:
            lines: List of file lines
            line_num: Line number to edit
            key: Metadata key
            value: New value (can be string, list, dict)

        Returns:
            Updated list of lines
        """
        # Parse the value to determine formatting
        parsed_value = self._parse_metadata_value(value)

        # Format the value
        if isinstance(parsed_value, list):
            value_str = f"[{', '.join(str(v) for v in parsed_value)}]"
        elif isinstance(parsed_value, dict):
            value_str = json.dumps(parsed_value)
        else:
            value_str = str(parsed_value)

        # Replace the line
        lines[line_num] = f"- {key}: {value_str}\n"
        return lines

    def _parse_metadata_value(self, value: Any) -> Any:
        """
        Parse a metadata value from string format.

        Handles:
        - List strings like "[a, b, c]" -> ['a', 'b', 'c']
        - Dict strings like '{"key": "value"}' -> {'key': 'value'}
        - Plain strings -> str

        Args:
            value: The value to parse (can be string or already parsed)

        Returns:
            Parsed value
        """
        if not isinstance(value, str):
            return value

        value = value.strip()

        # Try to parse as list
        if value.startswith('[') and value.endswith(']'):
            inner = value[1:-1]
            if inner.strip():
                return [x.strip() for x in inner.split(',')]
            else:
                return []

        # Try to parse as JSON dict
        if value.startswith('{') and value.endswith('}'):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value

        return value

    def _apply_content_edit(self, lines: List[str], start_line: int, end_line: int, new_content: str) -> List[str]:
        """
        Apply a content edit by replacing a range of lines.

        Args:
            lines: List of file lines
            start_line: Start of content block (inclusive)
            end_line: End of content block (exclusive)
            new_content: New content to insert

        Returns:
            Updated list of lines
        """
        # Split new content into lines, preserving line endings
        new_lines = []
        if new_content:
            # Split content but preserve structure
            content_lines = new_content.split('\n')
            for i, line in enumerate(content_lines):
                # Add newline to all lines except potentially the last
                if i < len(content_lines) - 1 or new_content.endswith('\n'):
                    new_lines.append(line + '\n')
                else:
                    new_lines.append(line)

        # Replace the range
        return lines[:start_line] + new_lines + lines[end_line:]


def apply_edits_to_file(edits: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Convenience function to apply edits to a file.

    Args:
        edits: Edit dictionary (see FileEditor.apply_edits for format)

    Returns:
        Tuple of (success: bool, message: str)
    """
    editor = FileEditor()
    return editor.apply_edits(edits)
